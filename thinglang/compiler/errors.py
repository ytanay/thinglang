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


class NoMatchingOverload(ThinglangException):
    """
    The method was not called with the expected number of arguments
    """

    def __init__(self, methods, arguments):
        super().__init__()
        self.methods, self.arguments = methods, arguments

    def __str__(self):
        return f'No matching overload for {self.methods[0].name} using arguments {self.arguments} was found.\n' + \
               f'Allowable overloads: {method.arguments for method in self.methods}.'

