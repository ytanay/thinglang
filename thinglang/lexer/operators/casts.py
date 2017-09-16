from thinglang.lexer.lexical_token import LexicalToken


class LexicalCast(LexicalToken):
    """
    A cast (conversion) operation between two types.

    Examples:
        "123" as number
        person as text
    """
