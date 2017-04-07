from thinglang.utils.exception_utils import ThinglangException


class UnresolvedReference(ThinglangException):
    pass


class DuplicateDeclaration(ThinglangException):
    pass


class ReturnInConstructorError(ThinglangException):
    pass


class EmptyMethodBody(ThinglangException):
    pass


class EmptyThingDefinition(ThinglangException):
    pass


class IndeterminateType(ThinglangException):
    pass


class ArgumentCountMismatch(ThinglangException):
    def __init__(self, expected, actual):
        super(ArgumentCountMismatch, self).__init__(expected, actual)
        self.expected = expected
        self.actual = actual
