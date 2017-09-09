import struct

from thinglang.compiler import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken, LexicalBinaryOperation


class LexicalNumericalValue(LexicalToken, ValueType):

    STATIC = True
    TYPE = LexicalIdentifier("number")
    TYPE_IDX = definitions.INTERNAL_TYPE_ORDERING[LexicalIdentifier("number")]

    def __init__(self, value, source_ref=None):
        super(LexicalNumericalValue, self).__init__(value, source_ref)
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

    def compile(self, context):
        ref = context.append_static(self.serialize())
        context.append(OpcodePushStatic(ref), self.source_ref)


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
