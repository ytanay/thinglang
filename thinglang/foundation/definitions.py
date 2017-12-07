from thinglang.lexer.values.identifier import Identifier

"""
The internal ordering of core types used by the compiler and runtime
"""

INTERNAL_TYPE_ORDERING = {
    Identifier("text"): 1,
    Identifier("number"): 2,
    Identifier("bool"): 3,
    Identifier("list"): 4,
    Identifier("Console"): 5,
    Identifier("File"): 6,
    Identifier("Time"): 7,
    Identifier("Exception"): 8,
    Identifier('iterator'): 9
}
