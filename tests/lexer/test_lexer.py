import pytest

from tests.infrastructure.test_utils import lexer_single
from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.base import LexicalIndent, LexicalIdentifier
from thinglang.parser.nodes.base import InlineString


UNTERMINATED_GROUPS = 'hello"', '"hello', 'hello`', '`hello', '"hello`', '`hello"'


def test_empty_string():
    symbols = lexer_single('""')

    assert len(symbols) == 2
    assert isinstance(symbols[0], InlineString) and symbols[0].value == ""


def test_whitespace_handling():
    assert lexer_single("does start with number a, number b, number c") == \
           lexer_single("does   start with number a,number b,number c   ")


def test_indentation_handling():
    assert lexer_single("\t\t\tid") == [LexicalIndent('\t')] * 3 + [LexicalIdentifier('id'), LexicalGroupEnd(None)]


@pytest.mark.parametrize('code', UNTERMINATED_GROUPS)
def test_group_termination_errors(code):
    with pytest.raises(ValueError):
        lexer_single(code)
