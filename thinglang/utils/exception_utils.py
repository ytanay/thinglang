class ThinglangException(Exception):

    def __init__(self):
        super(ThinglangException, self).__init__(self.message)

    @property
    def message(self):
        return f'Unknown exception: {type(self).__name__}'
