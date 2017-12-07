from thinglang.compiler.context import CompilationContext
from thinglang.lexer.definitions.tags import LexicalPrivateTag
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationMember
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.inline_code import InlineCode
from thinglang.symbols.symbol import Symbol


class MemberDefinition(BaseNode):
    """
    A member definition
    Must be a direct child of a ThingDefinition
    """

    def __init__(self, name, type_name, visibility=Symbol.PUBLIC):
        super(MemberDefinition, self).__init__([name, type_name])

        self.type, self.name, self.visibility = type_name, name, visibility

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())

    def symbol(self):
        return Symbol.member(self.name, self.type, self.visibility)

    def compile(self, context: CompilationContext):
        return

    MEMBER_NAME_TYPES = Identifier, InlineCode

    @staticmethod
    @ParserRule.mark
    def parse_member_definition(_: LexicalDeclarationMember, type_name: MEMBER_NAME_TYPES, name: Identifier):
        return MemberDefinition(name, type_name)

    @staticmethod
    @ParserRule.mark
    def tag_member_definition(_: LexicalPrivateTag, member: 'MemberDefinition'):
        member.visibility = Symbol.PRIVATE
        return member
