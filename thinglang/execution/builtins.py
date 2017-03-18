

class ITOutput(object):

    def __init__(self):
        self.data = ""

    def write(self, args):
        self.data += ' '.join(str(x) for x in args) + "\n"

    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        return hasattr(self, item)
