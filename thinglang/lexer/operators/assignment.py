from thinglang.lexer.lexical_token import LexicalToken


class LexicalAssignment(LexicalToken):
    """
    Signifies the assignment operator: =

    Examples:
        a = "hello"
        a = b
    """
