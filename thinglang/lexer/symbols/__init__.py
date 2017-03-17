import abc

from thinglang.common import Describable


class LexicalSymbol(Describable):
    EMITTABLE = True

    def __init__(self, raw):
        self.raw = raw

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def contextify(self, context):
        self.context = context
        return self


class LexicalBinaryOperation(LexicalSymbol, metaclass=abc.ABCMeta):
    def __init__(self, operator):
        super(LexicalBinaryOperation, self).__init__(operator)
        self.operator = operator


class LexicalGroupEnd(LexicalSymbol):
    pass