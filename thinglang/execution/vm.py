

class ITOutput(object):

    def __init__(self):
        self.data = ""

    def write(self, args):
        self.data += ' '.join(str(x) for x in args) + "\n"
        print(*args)

    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        return hasattr(self, item)


class Stack(object):

    def __init__(self):
        self.stack = []

    def __setitem__(self, key, value):
        print('Putting {} {}'.format(key, value))
        self.stack[-1][key] = value

    def __getitem__(self, item):
        print('State: {}'.format(self.stack))
        return self.stack[-1][item]

    def enter(self):
        self.stack.append({})

    def exit(self):
        return self.stack.pop()

HEAP = {
    "output": ITOutput()
}


STACK = Stack()