from thinglang.lexer.lexical_token import LexicalToken


class LexicalComparison(LexicalToken):
    """
    The binary and unary comparison operators (e.g. less than, greater than, equals, not, etc...)
    """

    @classmethod
    def transpile(cls):
        return cls.format_name()


class LexicalNegation(LexicalToken):
    """
    Specifies the negation operator, given by "not"
    """


class LexicalExclamation(LexicalToken):
    """
    Specifies the exclamation operator, given by "!"
    """


class LexicalEquals(LexicalComparison):
    """
    Signifies the equality operator, given by "eq"
    """


class LexicalNotEquals(LexicalComparison):
    """
    Specifies the inequality operator, given by "not eq"
    """


class LexicalGreaterThan(LexicalComparison):
    """
    Signifies the greater-than operator, given by ">"
    """


class LexicalLessThan(LexicalComparison):
    """
    Signifies the less-than operator, given by "<"
    """
