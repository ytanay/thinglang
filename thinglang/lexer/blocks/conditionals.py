from thinglang.lexer.lexical_token import LexicalToken


class LexicalConditional(LexicalToken):
    """
    The *if* conditional.

    Examples:
        if true
        if a eq b
    """


class LexicalElse(LexicalToken):
    """
    The *else* block.

    Examples:
        else
        else if a eq b
    """
