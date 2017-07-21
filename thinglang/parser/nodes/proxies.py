from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.functions import ArgumentListPartial, MethodCall, Access, ArgumentList
from thinglang.utils.type_descriptors import ValueType


class ConstrainedArithmeticOperation(object):

    @classmethod
    def construct(cls, slice):
        return ArgumentListPartial([None, ArithmeticOperation([slice[0][0], slice[1], slice[2][0]])])


class RangeGenerator(BaseNode, ValueType):

    @classmethod
    def construct(cls, slice):
        return MethodCall.create_constructing_call(LexicalIdentifier('Range'), ArgumentList([slice[0], slice[-1]]))


class TaggedLexicalDeclaration(BaseNode, ValueType):

    @classmethod
    def construct(cls, slice):
        slice[1].static_member = True
        return slice[1]
