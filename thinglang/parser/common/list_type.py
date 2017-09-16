from thinglang.parser.nodes.base_node import BaseNode


class ListInitialization(BaseNode):

    def __init__(self, slice=None):
        self.values = self.normalize_input(slice)

        super(ListInitialization, self).__init__(self.values)

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.values[key] = value

    def describe(self):
        return self.values

    @property
    def arguments(self):
        return self.values

    @staticmethod
    def normalize_input(value):
        if not value:
            return []

        if isinstance(value, list):
            return value

        return [value]
