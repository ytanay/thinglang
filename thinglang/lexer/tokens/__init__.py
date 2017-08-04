import abc

from thinglang.utils.describable import Describable


class LexicalToken(Describable):
    EMITTABLE = True
    STATIC = False
    ALLOW_EMPTY = False
    VECTOR_START, VECTOR_END = False, False

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

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.raw == other.raw and \
               self.value == other.value

    def __hash__(self):
        return hash((self.raw, self.value))


class LexicalBinaryOperation(LexicalToken):
    def __init__(self, operator):
        super(LexicalBinaryOperation, self).__init__(operator)
        self.operator = operator

    @classmethod
    def transpile(cls):
        return '__{}__'.format(cls.__name__)


class LexicalGroupEnd(LexicalToken):
    pass
