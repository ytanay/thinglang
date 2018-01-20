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
        return f'No matching overload for {self.methods[0].name} using arguments {[x.type for x in self.arguments]} was found.\n' + \
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


class NoExceptionHandlers(ThinglangException):
    """
    No exception handlers were registered for a try blck
    """

    def __init__(self, node):
        super().__init__()
        self.node = node

    def __str__(self):
        return f'No exception handling blocks were registered (at {self.node.source_ref})'


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
        return f'Cannot find reference {self.search.name}.{self.target} (at {self.original_target.source_ref})'


class SelfInStaticMethod(ThinglangException):
    """
    Reference to `self` in a static method
    """

    def __init__(self, target):
        super().__init__()
        self.target = target

    def __str__(self):
        return f'Usage of self in static method (at {self.target.source_ref})'


class UnfilledGenericParameters(ThinglangException):
    """
    A generic symbol map was selected without specifying type parameters
    """

    def __init__(self, target, container, element):
        super().__init__()
        self.container, self.element, self.target = container, element, target

    def __str__(self):
        return f'Usage of generic class {self.container.name}.{self.element.name if self.element else ""} without specifying parameter types (at {self.target.source_ref})'


class CalledInstanceMethodOnClass(ThinglangException):
    """
    An instance method was called on a class
    """

    def __init__(self, reference, source_ref):
        super().__init__()
        self.reference, self.source_ref = reference, source_ref

    def __str__(self):
        return f'Cannot call instance method on class {self.reference.type} (at {self.source_ref}'
