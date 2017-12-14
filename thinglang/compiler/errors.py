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
               f'Allowable overloads: {", ".join(str(method.arguments) for method in self.methods)}.'


class DuplicateHandlerError(ThinglangException):
    """
    Multiple handlers of the same exception type were registered
    """

    def __init__(self, handler_types):
        super().__init__()
        self.handler_types = handler_types

    def __str__(self):
        return f'Duplicate handlers were registered ({", ".join(str(handler_type) for handler_type in self.handler_types)})'

