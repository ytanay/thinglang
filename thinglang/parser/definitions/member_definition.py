from thinglang.compiler.context import CompilationContext
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationMember
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.inline_code import InlineCode
from thinglang.symbols.symbol import Symbol


class MemberDefinition(BaseNode):
    def __init__(self, name, type_name):
        super(MemberDefinition, self).__init__([name, type_name])

        self.type, self.name = type_name, name

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())

    def symbol(self):
        return Symbol.member(self.name, self.type)

    def compile(self, context: CompilationContext):
        return

    MEMBER_NAME_TYPES = Identifier, InlineCode

    @staticmethod
    @ParserRule.mark
    def parse_member_definition(_: LexicalDeclarationMember, type_name: MEMBER_NAME_TYPES, name: Identifier):
        return MemberDefinition(name, type_name)

