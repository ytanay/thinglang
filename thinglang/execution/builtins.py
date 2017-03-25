class ThingObjectBase(object):

    def __getitem__(self, item):

    def __contains__(self, item):
        return hasattr(self, item)



    def __init__(self):
        self.data = ""

    def write(self, args):
        self.data += ' '.join(str(x) for x in args) + "\n"

    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        return hasattr(self, item)
class ThingObjectInput(ThingObjectBase):

    def __init__(self):
        self.data = []

    def get_line(self):
        line = input()
        self.data.append(line)
        return line
