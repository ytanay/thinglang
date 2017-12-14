from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.operators.binary import LexicalAddition, LexicalSubtraction, LexicalMultiplication, \
    LexicalDivision, SecondOrderLexicalBinaryOperation, FirstOrderLexicalBinaryOperation
from thinglang.lexer.operators.comparison import LexicalEquals, LexicalGreaterThan, LexicalLessThan, LexicalComparison
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess
from thinglang.utils.type_descriptors import ValueType, CallSite


class BinaryOperation(BaseNode, ValueType, CallSite):
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
        self.operator, self.lhs, self.rhs = operator, lhs, rhs

    def compile(self, context: CompilationBuffer):
        method_call = MethodCall(NamedAccess.extend(self.lhs, Identifier(self.operator.transpile())), [self.rhs])
        return method_call.compile(context)

    def evaluate(self):
        return self.OPERATIONS[type(self.operator)](self.lhs.evaluate(), self.rhs.evaluate())

    def __repr__(self):
        return '{} {} {}'.format(self.lhs, self.operator, self.rhs)

    @property
    def arguments(self):
        return self.lhs, self.rhs

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
