from thinglang.lexer.lexical_token import LexicalToken


class LexicalBracketOpen(LexicalToken):
    """
    Signifies an opening bracket: [
    """


class LexicalBracketClose(LexicalToken):
    """
    Signifies a closing bracket: ]
    """

    MUST_CLOSE = True
