from thinglang.utils.exception_utils import ThinglangException


class TargetNotCallable(ThinglangException):
    """
    An attempt was made to call a target which is not a method, or is not callable.
    For example, attempting to call a class member
    """


class CapturedVoidMethod(ThinglangException):
    """
    An attempt was made to use the result of a void method.
    """


class ArgumentCountMismatch(ThinglangException):
    """
    The method was not called with the expected number of arguments
    """

    def __init__(self, expected_count, actual_count):
        self.expected_count, self.actual_count = expected_count, actual_count
        super(ArgumentCountMismatch, self).__init__()

    @property
    def message(self):
        return f'Wrong number of argument received. Expected {self.expected_count}, got {self.actual_count}'


class ArgumentTypeMismatch(ThinglangException):
    """
    The method was not called with the expected number of arguments
    """

    def __init__(self, target, index, expected_type, actual_type):
        self.target, self.index, self.expected_type, self.actual_type = target, index, expected_type, actual_type
        super(ArgumentTypeMismatch, self).__init__()

    @property
    def message(self):
        return f'{self.target}: Argument #{self.index + 1} is of incorrect type. Expected {self.expected_type}, got {self.actual_type}'

