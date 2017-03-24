from thinglang.execution.errors import UnknownVariable


class StackFrame(object):

    def __init__(self, instance):
        self.instance = instance
        self.data = {}
        self.idx = 0
        self.return_value = None

    def __setitem__(self, key, value):
        print('\tSET<{}> {}: {}'.format(self.idx, key, value))
        if key in self.data:
            self.data[key] = (self.data[key][0], value)
        else:
            self.data[key] = (self.idx, value)

    def __getitem__(self, item):
        if not item in self.data:
            raise UnknownVariable('Variable {} not recognized in this scope'.format(item))
        print('\tGET<{}> {}: {}'.format(self.idx, item, self.data[item][1]))
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
