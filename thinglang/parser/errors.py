from thinglang.utils.exception_utils import ThinglangException


class VectorReductionError(ThinglangException):
    """
    A generic parser error, thrown when a vector of lexical tokens could not be
    entirely reduced - that is to say, invalid syntax was supplied by the user.
    """
