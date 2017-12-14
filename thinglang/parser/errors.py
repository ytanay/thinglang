from typing import List

from thinglang.utils.exception_utils import ThinglangException


class VectorReductionError(ThinglangException):
    """
    A generic parser error, thrown when a vector of lexical tokens could not be
    entirely reduced - that is to say, invalid syntax was supplied by the user.
    """

    def __init__(self, reason: str, tokens: List):
        self.reason, self.tokens = reason, tokens
        super().__init__(str(self))

    def __str__(self):
        return f'{self.reason}: {self.tokens[0].source_ref}: {self.tokens}'


class InvalidIndexedAccess(ThinglangException):
    """
    Thrown when an invalid indexed access has been made.
    Examples:
        a[]
        a[1, 2, 3]
    """
