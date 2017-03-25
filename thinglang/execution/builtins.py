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

    def __init__(self):
        self.data = []

    def get_line(self):
        line = input()
        self.data.append(line)
        return line
