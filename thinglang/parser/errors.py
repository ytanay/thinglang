from typing import List

from thinglang.lexer.lexical_definitions import REVERSE_OPERATORS
from thinglang.utils.exception_utils import ThinglangException


class VectorReductionError(ThinglangException):
    """
    A generic parser error, thrown when a vector of lexical tokens could not be
    entirely reduced - that is to say, invalid syntax was supplied by the user.
    """

    def __init__(self, reason: str, tokens: List):
        super().__init__()
        self.reason, self.tokens = reason, tokens

    def __str__(self):
        return f'{self.reason}: {self.tokens[0].source_ref}: {self.tokens}'


class UnclosedVector(ThinglangException):
    """
    A token vector was not closed - mostly likely mising a closing ), ], }, etc...
    """

    def __init__(self, expected_token, depth, source_ref):
        super().__init__()
        self.expected_token, self.depth, self.source_ref = expected_token, depth, source_ref

    def __str__(self):
        return f'Missing closing token "{REVERSE_OPERATORS[self.expected_token]}" (at {self.source_ref}, depth {self.depth})'


class UnexpectedVectorTermination(ThinglangException):
    """
    A token vector was unnecessarily terminated  - most likely an extraneous ), ], }, etc...
    """

    def __init__(self, unexpected_token, source_ref):
        super().__init__()
        self.unexpected_token, self.source_ref = unexpected_token, source_ref

    def __str__(self):
        return f'Unexpected closing token "{REVERSE_OPERATORS[self.unexpected_token]}" (at {self.source_ref})'


class InvalidIndexedAccess(ThinglangException):
    """
    Thrown when an invalid indexed access has been made.
    Examples:
        a[]
        a[1, 2, 3]
    """


class StructureError(ThinglangException):
    def __init__(self, node, failing_children, required_types=None, negated=False):
        super().__init__()
        self.node, self.failing_children, self.required_types, self.negated = node, failing_children, required_types, negated

    def __str__(self):
        if self.required_types:
            return f'A {type(self.node).__name__} may {"not" if self.negated else "only"} contain {self.required_types}, but contains {self.failing_children} (at {self.node.source_ref})'
        else:
            return f'A {type(self.node).__name__} may {"not" if self.negated else "only"}  directly contain an {type(self.failing_children[0]).__name__} (at {self.node.source_ref})'


class CustomStructureError(StructureError):
    def __init__(self, node, message):
        super().__init__(node, None)
        self.message = message

    def __str__(self):
        return f'{self.message} (at {self.node.source_ref})'