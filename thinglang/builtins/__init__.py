from thinglang.lexer.tokens.base import LexicalIdentifier

TT_TEXT = LexicalIdentifier("Text", LexicalIdentifier.TYPE_INDICATOR)
TT_NUMBER = LexicalIdentifier("Number", LexicalIdentifier.TYPE_INDICATOR)

CORE_TYPES = {
    TT_TEXT,
    TT_NUMBER
}
