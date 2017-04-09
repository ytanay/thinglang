from thinglang.parser.symbols import BaseSymbol
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseSymbol):
    DECELERATION = object()
    REASSIGNMENT = object()
    INDETERMINATE = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        if len(slice) == 4:
            self.type, self.name, _, self.value = slice
            self.intent = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.intent = self.REASSIGNMENT
            self.type = self.INDETERMINATE

    def describe(self):
        return '{} {} = {}'.format(self.type, self.name, self.value)

    def references(self):
        if self.method is self.REASSIGNMENT:
            return self.name


class InlineString(ValueType):  # immediate string e.g. "hello world"
    def __init__(self, value):
        self.value = value

    def evaluate(self, _):
        return self.value

    def serialize(self):
        return self.evaluate(None)
