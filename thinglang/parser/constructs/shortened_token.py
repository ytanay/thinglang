from thinglang.parser.nodes import BaseNode
from thinglang.lexer.operators.assignment import LexicalAssignment
from thinglang.lexer.operators.comparison import LexicalEquals, LexicalExclamation, LexicalNotEquals
from thinglang.parser.rule import ParserRule
from thinglang.utils.source_context import SourceReference


class ShortenedTokens(BaseNode):

    def __init__(self):
        raise Exception('Do not instantiate ShortenedTokens')

    @staticmethod
    @ParserRule.mark # TODO: change this to have lexer look-ahead
    def parse_equality_shortcut(eq1: LexicalAssignment, eq2: LexicalAssignment):

        return LexicalEquals('==', SourceReference.combine([eq1, eq2]))

    @staticmethod
    @ParserRule.mark
    def parse_inequality_shortcut(exc: LexicalExclamation, eq: LexicalAssignment):
        return LexicalNotEquals('!=', SourceReference.combine([exc, eq]))
