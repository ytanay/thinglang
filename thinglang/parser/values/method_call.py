from thinglang.compiler.context import CompilationContext
from thinglang.compiler.errors import TargetNotCallable, ArgumentCountMismatch, ArgumentTypeMismatch
from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.statements.thing_instantiation import LexicalThingInstantiation
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.values.access import Access
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import ValueType


class MethodCall(BaseNode, ValueType):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)

        if isinstance(slice[0], LexicalThingInstantiation):
            self.target = Access([slice[1], Identifier.constructor()])
            self.arguments = ArgumentList(slice[2])
            self.constructing_call = True
        else:
            self.target, self.arguments = slice[0], ArgumentList(slice[1])
            self.constructing_call = False

        if not self.arguments:
            self.arguments = ArgumentList()

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)

    def replace_argument(self, idx, replacement):
        self.arguments[idx] = replacement

    @classmethod
    def create(cls, target, arguments=None):
        return cls([Access(target), arguments])

    def compile(self, context: CompilationContext):
        if self.target[0].implements(MethodCall):
            inner_target = self.target[0].compile(context)
            target = context.resolve(Access([inner_target.type, self.target[1]]))
        else:
            assert self.target.implements(Access)
            target = context.resolve(self.target.root)

            for ext, _ in self.target.extensions:
                target = context.resolve(target, ext)

            if target.kind != Symbol.METHOD:
                raise TargetNotCallable()

            if not target.static and not self.constructing_call:
                self.target.compile(context, without_last=True)

        expected_arguments = target.element.arguments

        if len(expected_arguments) != len(self.arguments):
            raise ArgumentCountMismatch(len(expected_arguments), len(self.arguments))

        for idx, (arg, expected_type) in enumerate(zip(self.arguments, expected_arguments)):
            compiled_target = arg.compile(context)

            if not self.validate_types(compiled_target, expected_type):
                raise ArgumentTypeMismatch(idx, expected_type, compiled_target.type)

        instruction = OpcodeCallInternal if target.convention is Symbol.INTERNAL else OpcodeCall
        context.append(instruction.type_reference(target), self.source_ref)

        if self.parent:
            context.append(OpcodePop(), self.source_ref)  # pop the return value, if the return value is not captured

        return target

    @staticmethod
    def validate_types(compiled_target, expected_type):
        if expected_type == Identifier('object'):
            return True

        return compiled_target.type == expected_type

