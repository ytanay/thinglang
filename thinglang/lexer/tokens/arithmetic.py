import struct

from thinglang.foundation import Foundation
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken, LexicalBinaryOperation


class LexicalNumericalValue(LexicalToken, ValueType):

    STATIC = True
    TYPE = LexicalIdentifier("number")
    TYPE_IDX = Foundation.INTERNAL_TYPE_ORDERING[LexicalIdentifier("number")]

    def __init__(self, value):
        super(LexicalNumericalValue, self).__init__(value)
        self.value = int(value)

    def evaluate(self, _=None):
        return self.value

    def describe(self):
        return self.value

    def serialize(self):
        return struct.pack('<ii', self.TYPE_IDX, self.value)

    @property
    def type(self):
        return self.TYPE


class FirstOrderLexicalBinaryOperation(LexicalBinaryOperation):  # addition, subtraction
    pass


class SecondOrderLexicalBinaryOperation(LexicalBinaryOperation):  # division, multiplication
    pass


class LexicalAddition(FirstOrderLexicalBinaryOperation):
    pass


class LexicalSubtraction(FirstOrderLexicalBinaryOperation):
    pass


class LexicalMultiplication(SecondOrderLexicalBinaryOperation):
    pass


class LexicalDivision(SecondOrderLexicalBinaryOperation):
    pass
