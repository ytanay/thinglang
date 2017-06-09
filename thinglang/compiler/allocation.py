class LinearMemoryAllocationLayout(object):
    def __init__(self, initial=None):
        initial = initial or {}
        self.mapping = initial
        self.next_index = len(initial)

    def add(self, name):
        index = self.next_index
        self.mapping[name] = self.next_index, name.type
        self.next_index += 1
        return index

    def get(self, name):
        return self.mapping[name]

    def __contains__(self, item):
        return self.mapping.__contains__(item)

