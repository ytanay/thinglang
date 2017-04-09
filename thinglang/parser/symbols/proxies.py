from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.functions import ArgumentListPartial, MethodCall, Access, ArgumentList
from thinglang.utils.type_descriptors import ValueType


class ConstrainedArithmeticOperation(object):

    @classmethod
    def construct(cls, slice):
        return ArgumentListPartial([None, ArithmeticOperation([slice[0][0], slice[1], slice[2][0]])])


class RangeGenerator(BaseSymbol, ValueType):

    @classmethod
    def construct(cls, slice):
        print(slice)
        return MethodCall.create_constructing_call(LexicalIdentifier('Range'), ArgumentList([slice[0], slice[-1]]))
