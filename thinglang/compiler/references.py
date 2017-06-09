class ResolvedReference(object):

    def __init__(self, index, type, original=None):
        self.index = index
        self.type = type
        self.original = original

    def transpile(self):
        return self.original.transpile()
