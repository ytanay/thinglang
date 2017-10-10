from thinglang.lexer.lexical_token import LexicalToken


class LexicalTry(LexicalToken):
    """
    A try block
    """


class LexicalHandle(LexicalToken):
    """
    The handling counterpart to the try block

    Examples:
        handle InvalidPathError ipe
    """
