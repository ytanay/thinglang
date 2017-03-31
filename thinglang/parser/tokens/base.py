from thinglang.parser.tokens import BaseToken
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseToken):
    DECELERATION = object()
    REASSIGNMENT = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        if len(slice) == 4:
            self.type, self.name, _, self.value = slice
            self.method = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.method = self.REASSIGNMENT
            self.type = 'INDETERMINATE'

    def describe(self):
        return '{} {} = {}'.format(self.type, self.name, self.value)


class InlineString(ValueType):  # immediate string e.g. "hello world"
    def __init__(self, value):
        self.value = value

    def evaluate(self, _):
        return self.value

    def serialize(self):
        return self.evaluate(None)

