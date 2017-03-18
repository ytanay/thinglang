from thinglang.common import ObtainableValue
from thinglang.parser.tokens import BaseToken


class ArithmeticOperation(BaseToken, ObtainableValue):
    OPERATIONS = {
        "+": lambda rhs, lhs: rhs + lhs,
        "*": lambda rhs, lhs: rhs * lhs,
        "-": lambda rhs, lhs: rhs - lhs,
        "/": lambda rhs, lhs: rhs / lhs
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.lhs, self.operator, self.rhs = slice

    def evaluate(self, stack):
        return self.OPERATIONS[self.operator.operator](self.lhs.evaluate(stack), self.rhs.evaluate(stack))

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def replace_argument(self, original, replacement):
        self.arguments = [replacement if x is original else x for x in self.arguments]

    def __getitem__(self, item):
        return self.arguments[item]