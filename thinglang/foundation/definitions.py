import itertools

from thinglang.lexer.values.identifier import Identifier

"""
The internal ordering of core types used by the compiler and runtime
"""

INTERNAL_TYPE_COUNTER = itertools.count(1)

# TODO: map dynamically at runtime

INTERNAL_TYPE_ORDERING = {
    Identifier("text"): next(INTERNAL_TYPE_COUNTER),
    Identifier("number"): next(INTERNAL_TYPE_COUNTER),
    Identifier("bool"): next(INTERNAL_TYPE_COUNTER),
    Identifier("list"): next(INTERNAL_TYPE_COUNTER),
    Identifier("map"): next(INTERNAL_TYPE_COUNTER),
    Identifier("iterator"): next(INTERNAL_TYPE_COUNTER),
    Identifier("Console"): next(INTERNAL_TYPE_COUNTER),
    Identifier("File"): next(INTERNAL_TYPE_COUNTER),
    Identifier("Time"): next(INTERNAL_TYPE_COUNTER),
    Identifier("Exception"): next(INTERNAL_TYPE_COUNTER)
}
