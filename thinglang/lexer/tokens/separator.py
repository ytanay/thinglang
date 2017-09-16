from thinglang.lexer.lexical_token import LexicalToken


class LexicalSeparator(LexicalToken):
    """
    Signifies a generic separator, given by a ",".

    Examples:
        [1, 2, 3]
        does add with number a, number b
    """