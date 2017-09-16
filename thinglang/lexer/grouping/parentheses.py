from thinglang.lexer.lexical_token import LexicalToken


class LexicalParenthesesOpen(LexicalToken):
    """
    Signifies an opening parentheses: (
    """


class LexicalParenthesesClose(LexicalToken):
    MUST_CLOSE = True

    """
    Signifies an closing parentheses: )
    """
