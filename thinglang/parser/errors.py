from thinglang.utils.exception_utils import ThinglangException


class ParseErrors(ThinglangException):
    pass


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
    pass