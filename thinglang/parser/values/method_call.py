from typing import Tuple

import collections

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.errors import TargetNotCallable, CapturedVoidMethod
from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodePop, OpcodeCallVirtual, OpcodeCallStatic
from thinglang.compiler.references import Reference, ElementReference
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.named_access import NamedAccess
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import ValueType, CallSite

CompiledArgument = collections.namedtuple('CompiledArgument', ['symbol', 'buffer'])


class MethodCall(BaseNode, ValueType, CallSite):
    """
    Represents a method call.
    Described by a target and an argument list.
    """

    STACK_ARGS = object()

    def __init__(self, target, arguments=None, stack_args=False, stack_target=False, is_captured=None):
        super(MethodCall, self).__init__([target, arguments])
        self.target, self.arguments, self.stack_args, self.stack_target, self._is_captured = target, (arguments if arguments is not None else ArgumentList()), stack_args, stack_target, is_captured

    def __repr__(self):
        return '{}({})'.format(self.target, self.arguments)

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.arguments == other.arguments

    def compile(self, context: CompilationBuffer):
        """
        Compiling method calls is probably the trickiest piece of logic in the thinglang compiler.
        We can separate the procedure into a number of distinct operations:

            1. Resolving the callable target (identified by self.target)
                If the first component of the target is a CallSite (i.e. we're looking at a chinaed method call),
                we compile it directly into the target buffer. Otherwise, we resolve it into an executable
                symbol, and compile a push down operation of the target instance
            2. Disambiguating the target symbol
                We now compile each argument in turn, producing a list of argument buffers and symbols. We use an
                ArgumentSelector to disambiguate between overloaded symbols (which also serves to validate types and
                produce an indication if an implicit cast is required)
            3. Calling convention selection
                Finally, we select the appropriate calling convention and merge the collected buffers.

        :param context:
        :return:
        """

        symbols, target_buffer = self.compile_target(context)
        final_ref, compiled_arguments = self.compile_arguments(context, symbols)

        for argument_type, argument_buffer in compiled_arguments:
            context.extend(argument_buffer)

        if not self.stack_target:
            context.extend(target_buffer)

        if final_ref.element.passthrough:
            return final_ref

        if final_ref.convention is Symbol.INTERNAL:
            instruction = OpcodeCallInternal
        elif final_ref.static or self.constructing_call:
            instruction = OpcodeCallStatic
        else:  # TODO: change this to elif target.is_part_of_inheritance_chain
            instruction = OpcodeCallVirtual

        context.append(instruction.type_reference(final_ref), self.source_ref)

        if final_ref.type is None and self.is_captured:
            raise CapturedVoidMethod()

        if final_ref.type is not None and not self.is_captured:
            context.append(OpcodePop(), self.source_ref)  # pop the return value, if the return value is not captured

        return final_ref

    def compile_target(self, context: CompilationBuffer) -> Tuple[ElementReference, CompilationBuffer]:
        assert isinstance(self.target, NamedAccess)

        target_buffer = context.optional()  # This buffer holds a push down operation for the target instance

        if isinstance(self.target[0], CallSite):
            assert not self.stack_target
            inner_target = self.target[0].compile(target_buffer)
            target = context.resolve(NamedAccess([inner_target.type, self.target[1]], tokens=self.target))
        else:
            target = context.resolve(self.target.root)

            for ext, _ in self.target.extensions:
                target = context.symbols.resolve_partial(target, ext)

            if target.kind != Symbol.METHOD:
                raise TargetNotCallable()

            if not target.static and not self.constructing_call and not self.stack_target:
                self.target.compile(target_buffer, without_last=True)

        return target, target_buffer

    def compile_arguments(self, context: CompilationBuffer, ref: ElementReference):
        argument_selector = ref.element.selector(context)
        compiled_arguments = []

        for idx, arg in enumerate(self.arguments):
            buffer = context.optional()
            compiled_target = arg if self.stack_args and isinstance(arg, Reference) else arg.compile(buffer)  # Deals with implicit casts
            argument_selector.constraint(compiled_target)
            compiled_arguments.append(CompiledArgument(compiled_target, buffer))

        selected = argument_selector.disambiguate(self.source_ref)
        ref.element = selected.symbol

        for (compiled_target, buffer), expected_type in zip(compiled_arguments, selected.symbol.arguments or []):
            if not argument_selector.inheritance_match(expected_type, compiled_target):
                MethodCall(NamedAccess([compiled_target.type, CastTag(expected_type)]), stack_target=True, is_captured=True)\
                    .deriving_from(self)\
                    .compile(buffer)

        return ref, compiled_arguments

    def deriving_from(self, node):
        self.target.deriving_from(node)
        return super().deriving_from(node)

    def replace_references(self, replacements):
        return MethodCall(self.target,
                          ArgumentList([x.replace_references(replacements) for x in self.arguments]),
                          self.stack_args,
                          self._is_captured) \
            .deriving_from(replacements.original)

    @property
    def is_captured(self):
        """
        Is the return value of this method call being used?
        """
        return self._is_captured if self._is_captured is not None else self.parent is None  # Check if this method call is directly in the AST

    @is_captured.setter
    def is_captured(self, value):
        self._is_captured = value

    @property
    def constructing_call(self):
        return self.target[-1] == Identifier.constructor()

    @staticmethod
    @ParserRule.mark
    def parse_method_call(target: NamedAccess, arguments: 'ParenthesesVector'):
        return MethodCall(target, ArgumentList(arguments))

    @staticmethod
    @ParserRule.mark
    def parse_instantiating_call(target: Identifier, arguments: 'ParenthesesVector'):
        return MethodCall(NamedAccess.extend(target, Identifier.constructor()), ArgumentList(arguments))

