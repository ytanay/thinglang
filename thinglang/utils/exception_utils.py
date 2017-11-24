class ThinglangException(Exception):
    """
    The base thinglang exception class
    """

    def __init__(self, *args):
        self.args = args
        super(ThinglangException, self).__init__(self.message)

    @property
    def message(self):
        return f'{type(self).__name__}: {self.args}'
