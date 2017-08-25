class ThinglangException(Exception):

    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args
