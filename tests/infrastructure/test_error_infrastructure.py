from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import UnresolvedReference


def test_error_infrastructure():
    assert UnresolvedReference(LexicalIdentifier("a")) == UnresolvedReference(LexicalIdentifier("a"))
    assert UnresolvedReference(LexicalIdentifier("a")) != UnresolvedReference(LexicalIdentifier("b"))
