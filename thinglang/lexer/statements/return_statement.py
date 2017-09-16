from thinglang.lexer.lexical_token import LexicalToken


class LexicalReturnStatement(LexicalToken):
    """
    Returns from a method.

    Examples:
        return
        return 1
    """
