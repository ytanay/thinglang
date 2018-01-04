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

    def __init__(self, methods, arguments, exact_matches, inheritance_matches, cast_matches, source_ref):
        super().__init__()
        self.methods, self.arguments, self.exact_matches, self.inheritance_matches, self.cast_matches, self.source_ref = \
            methods, arguments, exact_matches, inheritance_matches, cast_matches, source_ref

    def __str__(self):
        return f'No matching overload for {self.methods[0].name} using arguments {self.arguments} was found.\n' + \
               f'Allowable overloads: {", ".join(str(method.arguments) for method in self.methods)}.\n' + \
               f'At {self.source_ref}'


class DuplicateHandlerError(ThinglangException):
    """
    Multiple handlers of the same exception type were registered
    """

    def __init__(self, handler_types):
        super().__init__()
        self.handler_types = handler_types

    def __str__(self):
        return f'Duplicate handlers were registered ({", ".join(str(handler_type) for handler_type in self.handler_types)})'


class ExceptionSpecificityError(ThinglangException):
    """
    A handler for an exception was registered after a handler that also catches it.
    """

    def __init__(self, specified_exception, prior):
        super().__init__()
        self.specified_exception, self.prior = specified_exception, prior

    def __str__(self):
        return f'The exception handler for {self.specified_exception} cannot be reached. ' \
               f'Exceptions of this type will be handled by the handler for {self.prior}.'


class InvalidReference(ThinglangException):
    """
    Reference to an invalid entity - e.g., missing member or method
    """

    def __init__(self, target, search, original_target):
        super().__init__()
        self.target, self.search, self.original_target = target, search, original_target

    def __str__(self):
        return f'{self.target} does not exist in {self.search.name} (at {self.original_target.source_ref})'


class SelfInStaticMethod(ThinglangException):
    """
    Reference to `self` in a static method
    """

    def __init__(self, target):
        super().__init__()
        self.target = target

    def __str__(self):
        return f'Usage of self in static method (at {self.target.source_ref})'
