from thinglang.lexer.lexical_definitions import REVERSE_OPERATORS
from thinglang.lexer.operators.binary import LexicalAddition, LexicalSubtraction, LexicalMultiplication, \
    LexicalDivision, SecondOrderLexicalBinaryOperation, FirstOrderLexicalBinaryOperation
from thinglang.lexer.operators.comparison import LexicalEquals, LexicalGreaterThan, LexicalLessThan, LexicalComparison
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class BinaryOperation(BaseNode, ValueType):
    """
    Represents binary operations (arithmetic and logic)
    """

    OPERATIONS = {
        LexicalAddition: lambda lhs, rhs: lhs + rhs,
        LexicalMultiplication: lambda lhs, rhs: lhs * rhs,
        LexicalSubtraction: lambda lhs, rhs: lhs - rhs,
        LexicalDivision: lambda lhs, rhs: lhs / rhs,
        LexicalEquals: lambda lhs, rhs: lhs == rhs,
        LexicalGreaterThan: lambda lhs, rhs: lhs > rhs,
        LexicalLessThan: lambda lhs, rhs: lhs < rhs
    }

    def __init__(self, operator, lhs, rhs):
        super(BinaryOperation, self).__init__([operator, lhs, rhs])
        self.arguments = [lhs, rhs]
        self.operator = type(operator)

    def __getitem__(self, item):
        return self.arguments[item]

    def evaluate(self):
        return self.OPERATIONS[self.operator](self[0].evaluate(), self[1].evaluate())

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def transpile(self):
        return '{} {} {}'.format(self.arguments[0].transpile(), REVERSE_OPERATORS[self.operator], self.arguments[1].transpile())

    @staticmethod
    @ParserRule.mark
    def parse_second_order_operation(lhs: ValueType, operator: SecondOrderLexicalBinaryOperation, rhs: ValueType):
        return BinaryOperation(operator, lhs, rhs)

    @staticmethod
    @ParserRule.mark
    def parse_first_order_operation(lhs: ValueType, operator: FirstOrderLexicalBinaryOperation, rhs: ValueType):
        return BinaryOperation(operator, lhs, rhs)

    @staticmethod
    @ParserRule.mark
    def parse_comparison_operation(lhs: ValueType, operator: LexicalComparison, rhs: ValueType):
        return BinaryOperation(operator, lhs, rhs)
