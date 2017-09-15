class TargetNotCallable(Exception):
    """
    An attempt was made to call a target which is not a method, or is not callable.
    For example, attempting to call a class member
    """


class ArgumentCountMismatch(Exception):
    """
    The method was not called with the expected number of arguments
    """

    def __init__(self, expected_count, actual_count):
        super(ArgumentCountMismatch, self).__init__()
        self.expected_count, self.actual_count = expected_count, actual_count


class ArgumentTypeMismatch(Exception):
    """
    The method was not called with the expected number of arguments
    """

    def __init__(self, index, expected_type, actual_type):
        super(ArgumentTypeMismatch, self).__init__()
        self.index, self.expected_type, self.actual_type = index, expected_type, actual_type
