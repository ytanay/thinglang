from thinglang.lexer.lexical_token import LexicalToken


class LexicalBinaryOperation(LexicalToken):
    """
    The base binary operation: an operation with two operands
    """
    def __init__(self, value, source_ref):
        super(LexicalBinaryOperation, self).__init__(value, source_ref)
        self.operator = value

    @classmethod
    def transpile(cls):
        return cls.format_name()


class FirstOrderLexicalBinaryOperation(LexicalBinaryOperation):
    """
    Describes the first order binary operations: addition and subtraction
    """


class SecondOrderLexicalBinaryOperation(LexicalBinaryOperation):
    """
    Describes the second order binary operations: multiplication and division
    """


class LexicalAddition(FirstOrderLexicalBinaryOperation):
    """
    Addition, using +
    """


class LexicalSubtraction(FirstOrderLexicalBinaryOperation):
    """
    Subtraction, using -
    """


class LexicalMultiplication(SecondOrderLexicalBinaryOperation):
    """
    Multiplication, using *
    """


class LexicalDivision(SecondOrderLexicalBinaryOperation):
    """"
    Division, using /
    """


class LexicalModulus(SecondOrderLexicalBinaryOperation):
    """
    Modulus, using %
    """


class LexicalBinaryAnd(SecondOrderLexicalBinaryOperation):
    """
    AND, using &
    """


class LexicalBinaryOr(SecondOrderLexicalBinaryOperation):
    """
    OR, using |
    """


class LexicalBinaryXOR(SecondOrderLexicalBinaryOperation):
    """
    Exclusive-OR (XOR), using ^
    """