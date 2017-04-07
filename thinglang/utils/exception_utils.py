class ThinglangException(Exception):

    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args

    def __hash__(self):
        return super(ThinglangException, self).__hash__()