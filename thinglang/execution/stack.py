from thinglang.execution.errors import UnknownVariable
from thinglang.lexer.symbols.base import LexicalIdentifier


class Stack(object):
    def __init__(self):
        self.frames = []

    def __getitem__(self, item):
        return self.frames[-1][item]

    def __setitem__(self, key, value):
        self.frames[-1][key] = value

    def __contains__(self, item):
        return item in self.frames[-1]

    def __iter__(self):
        return iter(self.frames[-1])

    def push(self, frame):
        self.frames.append(frame)

    def pop(self):
        return self.frames.pop()

    def __getattr__(self, item):
        return getattr(self.frames[-1], item)

    def __str__(self):
        return f'Stack<{len(self.frames)}>(locals={self.data}, instance={self.instance})'


class Frame(object):

    def __init__(self, instance):
        self.instance = instance
        self.data = {}
        self.idx = 0
        self.return_value = None

    def returns(self, value):
        self.return_value = value

    def __setitem__(self, key, value):
        print('\tSET<{}> {}: {}'.format(self.idx, key, value))
        assert isinstance(key, LexicalIdentifier)
        if key in self.data:
            self.data[key] = (self.data[key][0], value)
        else:
            self.data[key] = (self.idx, value)

    def __getitem__(self, item):

        if not item in self.data:
            raise UnknownVariable('Variable {} not recognized in this scope'.format(item))
        print('\tGET<{}> {}: {}'.format(self.idx, item, self.data[item][1]))
        assert isinstance(item, LexicalIdentifier)
        return self.data[item][1]

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        for key, value in self.data.items():
            yield key, value

    def enter(self):
        print('\tINCR<{}> -> <{}>'.format(self.idx, self.idx + 1))
        self.idx += 1

    def exit(self):
        assert self.idx > 0, 'Cannot exit lowest stack segment'
        print('\tDECR<{}> -> <{}>'.format(self.idx, self.idx - 1))
        self.data = {
            key: value for key, value in self.data.items() if value[0] != self.idx
        }

        self.idx -= 1


class StackFrameTerminator(object):
    def __init__(self, target_arg=None):
        self.target_arg = target_arg


class StackScopeTerminator(object):
    pass
