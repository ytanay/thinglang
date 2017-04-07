from thinglang.lexer.tokens.base import LexicalIdentifier

INTERNAL_MEMBER = object()


class ThingObjectMeta(type):
    def __new__(mcs, name, bases, dct):
        if bases[0] is not object:
            dct['EXPORTS'] = {LexicalIdentifier(k): INTERNAL_MEMBER for k, v in dct.items() if not k.startswith('_') and callable(v)}

        return super(ThingObjectMeta, mcs).__new__(mcs, name, bases, dct)


class ThingObjectBase(object, metaclass=ThingObjectMeta):

    def __getitem__(self, item):
        return getattr(self, item.value)

    def __contains__(self, item):
        return hasattr(self, item.value)


class ThingObjectOutput(ThingObjectBase):
    INTERNAL_NAME = "Output"

    def __init__(self, heap):
        self.data = []
        self.heap = heap

    def write(self, *args):
        self.data.append(' '.join(str(x) for x in args))


class ThingObjectInput(ThingObjectBase):
    INTERNAL_NAME = "Input"

    def __init__(self, heap):
        self.data = []
        self.heap = heap

    def get_line(self, line=None):
        if line is not None:
            self.heap[LexicalIdentifier('Output')].write(line)

        line = input()
        self.data.append(line)
        return line


BUILTINS = ThingObjectOutput, ThingObjectInput

