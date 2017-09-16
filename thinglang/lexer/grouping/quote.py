from thinglang.lexer.lexical_token import LexicalToken


class LexicalQuote(LexicalToken):  # "
    """
    Signifies a regular quote: "
    """

    EMITTABLE = False
    ALLOW_EMPTY = True

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'"': LexicalQuote}
        return original
