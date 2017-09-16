from thinglang.lexer.lexical_token import LexicalToken


class LexicalBacktick(LexicalToken):
    """
    Signifies a backtick: `

    Used for inlining C++ code.
    """

    EMITTABLE = False
    ALLOW_EMPTY = True

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'`': LexicalBacktick}
        return original
