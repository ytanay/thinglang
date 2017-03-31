class ThingObjectBase(object):

    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        return hasattr(self, item)


class ThingObjectOutput(ThingObjectBase):

    def __init__(self):
        self.data = []

    def write(self, *args):
        self.data.append(' '.join(str(x) for x in args))


class ThingObjectInput(ThingObjectBase):

    def __init__(self, heap):
        self.data = []
        self.heap = heap

    def get_line(self, line=None):
        if line is not None:
            self.heap['Output'].write(line)

        line = input()
        self.data.append(line)
        return line
