from thinglang.lexer.definitions.tags import LexicalPrivateTag
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationMember
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.symbols.symbol import Symbol


class MemberDefinition(BaseNode):
    """
    A member definition
    Must be a direct child of a ThingDefinition
    """

    def __init__(self, name, type_name, visibility=Symbol.PUBLIC):
        super(MemberDefinition, self).__init__([name, type_name])

        self.type, self.name, self.visibility = type_name, name, visibility

    def __repr__(self):
        return 'has {} {}'.format(self.type, self.name)

    def symbol(self):
        return Symbol.member(self.name, self.type, self.visibility)

    MEMBER_NAME_TYPES = Identifier

    @staticmethod
    @ParserRule.mark
    def parse_member_definition(_: (LexicalDeclarationMember, LexicalPrivateTag), type_name: MEMBER_NAME_TYPES, name: Identifier):
        return MemberDefinition(name, type_name)
