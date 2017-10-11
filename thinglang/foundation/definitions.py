from thinglang.lexer.values.identifier import Identifier

INTERNAL_TYPE_ORDERING = {
    Identifier("text"): 1,
    Identifier("number"): 2,
    Identifier("bool"): 3,
    Identifier("list"): 4,
    Identifier("Console"): 5,
    Identifier("File"): 6
}
