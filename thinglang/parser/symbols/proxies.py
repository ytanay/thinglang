from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.functions import ArgumentListPartial


class ConstrainedArithmeticOperation(object):

    @classmethod
    def construct(cls, slice):
        return ArgumentListPartial([None, ArithmeticOperation([slice[0][0], slice[1], slice[2][0]])])
