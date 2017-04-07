from thinglang.utils.exception_utils import ThinglangException


class UnresolvedReference(ThinglangException):
    pass


class RedeclaredVariable(ThinglangException):
    pass


class ReturnInConstructorError(ThinglangException):
    pass


class EmptyMethodBody(ThinglangException):
    pass


class EmptyThingDefinition(ThinglangException):
    pass


class ArgumentCountMismatch(ThinglangException):
    pass