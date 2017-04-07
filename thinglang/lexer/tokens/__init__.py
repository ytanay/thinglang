import abc

from thinglang.utils.describable import Describable


class LexicalToken(Describable):
    EMITTABLE = True

    def __init__(self, raw):
        self.raw = raw
        self.context = None

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def contextify(self, context):
        self.context = context
        return self


class LexicalBinaryOperation(LexicalToken, metaclass=abc.ABCMeta):
    def __init__(self, operator):
        super(LexicalBinaryOperation, self).__init__(operator)
        self.operator = operator


class LexicalGroupEnd(LexicalToken):
    pass