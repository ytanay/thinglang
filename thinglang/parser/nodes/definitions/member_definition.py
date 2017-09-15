from thinglang.compiler.context import CompilationContext
from thinglang.parser.nodes import BaseNode
from thinglang.symbols.symbol import Symbol


class MemberDefinition(BaseNode):
    def __init__(self, slice):
        super(MemberDefinition, self).__init__(slice)

        _, self.type, self.name = slice

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())

    def symbol(self):
        return Symbol.member(self.name, self.type)

    def compile(self, context: CompilationContext):
        return
