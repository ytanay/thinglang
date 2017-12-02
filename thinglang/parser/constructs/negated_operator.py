from thinglang.lexer.operators.comparison import LexicalNegation, LexicalComparison, LexicalEquals, LexicalNotEquals
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class NegatedOperation(BaseNode):
    """
    Negates a comparison operation
    """

    @staticmethod
    @ParserRule.mark
    def parse_instantiating_call(_: LexicalNegation, op: LexicalComparison):
        if isinstance(op, LexicalEquals):
            return LexicalNotEquals(op.value, op.source_ref)
