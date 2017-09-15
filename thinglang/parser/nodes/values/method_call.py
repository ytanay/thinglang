from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop
from thinglang.lexer import LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalClassInitialization
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.definitions.argument_list import ArgumentList
from thinglang.parser.nodes.values.access import Access
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import ValueType


class MethodCall(BaseNode, ValueType):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)

        if isinstance(slice[0], LexicalClassInitialization):
            self.target = Access([slice[1], LexicalIdentifier.constructor()])
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

    def compile(self, context: CompilationContext, captured=False):
        if self.target[0].implements(MethodCall):
            inner_target = self.target[0].compile(context, True)
            target = context.resolve(Access([inner_target.type, self.target[1]]))
        elif self.target.implements(Access):
            target = context.resolve(self.target.root)

            for ext, _ in self.target.extensions:
                target = context.resolve(target, ext)

            assert target.kind == Symbol.METHOD, 'Target is not callable'

            if not target.static and not self.constructing_call:
                self.target.compile(context, without_last=True)

        else:
            raise Exception('Cannot call method on target {}'.format(self.target))

        for arg in self.arguments:
            arg.compile(context)

        instruction = OpcodeCallInternal if target.convention is Symbol.INTERNAL else OpcodeCall
        context.append(instruction.type_reference(target), self.source_ref)

        if self.parent:
            context.append(OpcodePop(), self.source_ref)  # pop the return value, if the return value is not captured

        return target
