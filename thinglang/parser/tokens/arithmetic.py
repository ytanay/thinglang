from thinglang.common import ValueType
from thinglang.parser.tokens import BaseToken


class ArithmeticOperation(BaseToken, ValueType):
    OPERATIONS = {
        "+": lambda rhs, lhs: rhs + lhs,
        "*": lambda rhs, lhs: rhs * lhs,
        "-": lambda rhs, lhs: rhs - lhs,
        "/": lambda rhs, lhs: rhs / lhs
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.arguments = [slice[0], slice[2]]
        self.operator = slice[1]

    def evaluate(self, stack):
        return self.OPERATIONS[self.operator.operator](self[0].evaluate(stack), self[1].evaluate(stack))

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def replace_argument(self, original, replacement):
        self.arguments = [replacement if x is original else x for x in self.arguments]

    def __getitem__(self, item):
        return self.arguments[item]