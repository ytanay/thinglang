from thinglang.parser.nodes import BaseNode


class ListInitialization(BaseNode):

    def __init__(self, slice=None):
        super(ListInitialization, self).__init__(slice if isinstance(slice, list) else ([slice] if slice else ()))

        if not slice:
            self.arguments = []
        elif isinstance(slice, list):
            self.arguments = slice
        else:
            self.arguments = [slice]

    def __iter__(self):
        return iter(self.arguments)

    def __len__(self):
        return len(self.arguments)

    def __getitem__(self, item):
        return self.arguments[item]

    def __setitem__(self, key, value):
        self.arguments[key] = value

    def describe(self):
        return self.arguments
