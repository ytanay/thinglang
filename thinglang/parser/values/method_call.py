from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.errors import TargetNotCallable, ArgumentCountMismatch, ArgumentTypeMismatch, CapturedVoidMethod
from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop
from thinglang.lexer.statements.thing_instantiation import LexicalThingInstantiation
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.named_access import NamedAccess
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import ValueType, CallSite


class MethodCall(BaseNode, ValueType, CallSite):
    """
    Represents a method call.
    Described by a target and an argument list.
    """

    STACK_ARGS = object()

    def __init__(self, target, arguments=None):
        super(MethodCall, self).__init__([target, arguments])
        self.target, self.arguments = target, (arguments if arguments is not None else ArgumentList())

    def __repr__(self):
        return '{}({})'.format(self.target, self.arguments)

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.arguments == other.arguments

    def replace_argument(self, idx, replacement):
        self.arguments[idx] = replacement

    def compile(self, context: CompilationBuffer):
        if isinstance(self.target[0], MethodCall):
            inner_target = self.target[0].compile(context)
            target = context.resolve(NamedAccess([inner_target.type, self.target[1]]))
        else:
            assert isinstance(self.target, NamedAccess)
            target = context.resolve(self.target.root)

            for ext, _ in self.target.extensions:
                target = context.symbols.resolve_partial(target, ext)

            if target.kind != Symbol.METHOD:
                raise TargetNotCallable()

            if not target.static and not self.constructing_call:
                self.target.compile(context, without_last=True)

        expected_arguments = target.element.arguments

        if self.arguments is not MethodCall.STACK_ARGS:

            if len(expected_arguments) != len(self.arguments):
                raise ArgumentCountMismatch(len(expected_arguments), len(self.arguments))

            for idx, (arg, expected_type) in enumerate(zip(self.arguments, expected_arguments)):
                compiled_target = arg.compile(context)

                if not self.validate_types(compiled_target, expected_type):
                    raise ArgumentTypeMismatch(target, idx, expected_type, compiled_target.type)

        instruction = OpcodeCallInternal if target.convention is Symbol.INTERNAL else OpcodeCall
        context.append(instruction.type_reference(target), self.source_ref)

        if target.type is None and self.is_captured:
            raise CapturedVoidMethod()

        if target.type is not None and not self.is_captured:
            context.append(OpcodePop(), self.source_ref)  # pop the return value, if the return value is not captured

        return target

    @property
    def is_captured(self):
        """
        Is the return value of this method call being used?
        """
        return self.parent is None  # Check if this method call is directly in the AST

    @staticmethod
    def validate_types(compiled_target, expected_type):
        if expected_type == Identifier('object'):
            return True

        return compiled_target.type == expected_type

    @property
    def constructing_call(self):
        return self.target[-1] == Identifier.constructor()

    @staticmethod
    @ParserRule.mark
    def parse_method_call(target: NamedAccess, arguments: 'ParenthesesVector'):
        return MethodCall(target, ArgumentList(arguments))

    # TODO: remove this syntax
    @staticmethod
    @ParserRule.mark
    def parse_instantiating_call(_: LexicalThingInstantiation, type_name: Identifier, arguments: 'ParenthesesVector'):
        return MethodCall(NamedAccess([type_name, Identifier.constructor()]), ArgumentList(arguments))
