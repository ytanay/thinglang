from thinglang.lexer.lexical_definitions import REVERSE_OPERATORS
from thinglang.lexer.tokens.arithmetic import LexicalAddition, LexicalMultiplication, LexicalSubtraction, \
    LexicalDivision
from thinglang.lexer.tokens.logic import LexicalEquals, LexicalInequality, LexicalGreaterThan, LexicalLessThan
from thinglang.parser.nodes import BaseNode
from thinglang.utils.type_descriptors import ValueType


class BinaryOperation(BaseNode, ValueType):
    OPERATIONS = {
        LexicalAddition: lambda lhs, rhs: lhs + rhs,
        LexicalMultiplication: lambda lhs, rhs: lhs * rhs,
        LexicalSubtraction: lambda lhs, rhs: lhs - rhs,
        LexicalDivision: lambda lhs, rhs: lhs / rhs,
        LexicalEquals: lambda lhs, rhs: lhs == rhs,
        LexicalInequality: lambda lhs, rhs: lhs != rhs,
        LexicalGreaterThan: lambda lhs, rhs: lhs > rhs,
        LexicalLessThan: lambda lhs, rhs: lhs < rhs
    }

    def __init__(self, slice):
        super(BinaryOperation, self).__init__(slice)
        self.arguments = [slice[0], slice[2]]
        self.operator = type(slice[1])

    def __getitem__(self, item):
        return self.arguments[item]

    def evaluate(self):
        return self.OPERATIONS[self.operator](self[0].evaluate(), self[1].evaluate())

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def transpile(self):
        return '{} {} {}'.format(self.arguments[0].transpile(), REVERSE_OPERATORS[self.operator], self.arguments[1].transpile())
