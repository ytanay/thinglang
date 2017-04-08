from thinglang.parser.errors import UnresolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier


def test_error_infrastructure():
    assert UnresolvedReference(LexicalIdentifier("a")) == UnresolvedReference(LexicalIdentifier("a"))
    assert UnresolvedReference(LexicalIdentifier("a")) != UnresolvedReference(LexicalIdentifier("b"))
