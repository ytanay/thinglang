from thinglang.common import ImmediateValue
from thinglang.lexer.symbols import LexicalSymbol, LexicalBinaryOperation


class LexicalNumericalValue(LexicalSymbol, ImmediateValue):
    def __init__(self, value):
        super(LexicalNumericalValue, self).__init__(value)
        self.value = int(value)

    def evaluate(self, stack):
        return self.value


class FirstOrderLexicalBinaryOperation(LexicalBinaryOperation):  # addition, subtraction
    pass


class SecondOrderLexicalBinaryOperation(LexicalBinaryOperation): # division, multiplication
    pass
