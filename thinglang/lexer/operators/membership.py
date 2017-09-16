from thinglang.lexer.lexical_token import LexicalToken


class LexicalIn(LexicalToken):
    """
    Checks for and refers to membership.

    Examples:
        2 in [1, 2, 3]
        for a in [1, 2, 3]
    """
