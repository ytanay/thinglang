from thinglang.lexer.lexical_token import LexicalToken


class LexicalAccess(LexicalToken):
    """
    Signifies a reference.

    Examples:
        person.name
        person.walk
        Number.from
    """
