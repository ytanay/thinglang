class ValueType(object):
    pass


class ReplaceableArguments(object):

    def replace(self, original, replacement):
        self.arguments = [replacement if x is original else x for x in self.arguments]
