import abc

from thinglang.utils.describable import Describable


class LexicalToken(Describable):
    EMITTABLE = True
    ALLOW_EMPTY = False

    def __init__(self, raw, value=None):
        self.raw = raw
        self.value = value
        self.context = None

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def set_context(self, context):
        self.context = context
        return self

    def references(self):
        return ()

    def transpile(self):
        return self.value


class LexicalBinaryOperation(LexicalToken, metaclass=abc.ABCMeta):
    def __init__(self, operator):
        super(LexicalBinaryOperation, self).__init__(operator)
        self.operator = operator


class LexicalGroupEnd(LexicalToken):
    pass
