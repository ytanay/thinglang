from thinglang.lexer.lexical_token import LexicalToken


class LexicalThrowStatement(LexicalToken):
    """
    Throws an exception

    Examples:
        throw create FileNotFoundError(path)
    """
