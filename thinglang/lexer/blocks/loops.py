from thinglang.lexer.lexical_token import LexicalToken


class LexicalRepeatFor(LexicalToken):
    """
    The *for* loop.

    Examples:
        for a in b
        for a in [1, 2, 3]
    """


class LexicalRepeatWhile(LexicalToken):  # repeat while
    """
    The *while* loop.

    Examples:
        while true
        while a eq b
    """
