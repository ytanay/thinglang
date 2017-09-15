from thinglang.lexer.tokens.base import LexicalIdentifier

INTERNAL_TYPE_ORDERING = {
    LexicalIdentifier("none"): 0,
    LexicalIdentifier("text"): 1,
    LexicalIdentifier("number"): 2,
    LexicalIdentifier("bool"): 3,
    LexicalIdentifier("Output"): 4
}