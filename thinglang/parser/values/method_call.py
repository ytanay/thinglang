from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.errors import TargetNotCallable, CapturedVoidMethod
from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop
from thinglang.compiler.references import Reference
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.named_access import NamedAccess
from thinglang.phases import preprocess
from thinglang.symbols.symbol import Symbol
from thinglang.utils.source_context import SourceContext
from thinglang.utils.type_descriptors import ValueType, CallSite


class MethodCall(BaseNode, ValueType, CallSite):
    """
    Represents a method call.
    Described by a target and an argument list.
    """

    STACK_ARGS = object()

    def __init__(self, target, arguments=None, stack_args=False, is_captured=None):
        super(MethodCall, self).__init__([target, arguments])
        self.target, self.arguments, self.stack_args, self._is_captured = target, (arguments if arguments is not None else ArgumentList()), stack_args, is_captured

    def __repr__(self):
        return '{}({})'.format(self.target, self.arguments)

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.arguments == other.arguments

    def compile(self, context: CompilationBuffer):

        target = self.final_target(context)

        self.compile_target(context)
        self.compile_arguments(target, context)
        instruction = OpcodeCallInternal if target.convention is Symbol.INTERNAL else OpcodeCall
        context.append(instruction.type_reference(target), self.source_ref)

        if target.type is None and self.is_captured:
            raise CapturedVoidMethod()

        if target.type is not None and not self.is_captured:
            context.append(OpcodePop(), self.source_ref)  # pop the return value, if the return value is not captured

        return target

    def compile_target(self, context: CompilationBuffer):
        assert isinstance(self.target, NamedAccess)

        if isinstance(self.target[0], CallSite):
            inner_target = self.target[0].compile(context)
            target = context.resolve(NamedAccess([inner_target.type, self.target[1]]))
        else:
            target = context.resolve(self.target.root)

            for ext, _ in self.target.extensions:
                target = context.symbols.resolve_partial(target, ext)

            if target.kind != Symbol.METHOD:
                raise TargetNotCallable()

            if not target.static and not self.constructing_call:
                self.target.compile(context, without_last=True)

        return target

    def compile_arguments(self, target, context: CompilationBuffer):
        argument_selector = target.element.selector()

        for idx, arg in enumerate(self.arguments):
            compiled_target = arg if self.stack_args and isinstance(arg, Reference) else arg.compile(context)  # Deals with implicit casts
            argument_selector.constraint(compiled_target, self.source_ref)

        target.element = argument_selector.disambiguate(self.source_ref)

        return target

    def final_target(self, context):
        ambiguous_target = self.compile_target(context.optional())
        return self.compile_arguments(ambiguous_target, context.optional())

    def deriving_from(self, node):
        self.target.deriving_from(node)
        return super().deriving_from(node)

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

