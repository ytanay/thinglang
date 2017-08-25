import pytest

from thinglang.lexer.lexer import analyze_line
from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.base import LexicalIndent
from thinglang.parser.nodes.base import InlineString

UNTERMINATED_GROUPS = 'hello"', '"hello', 'hello`', '`hello', '"hello`', '`hello"'


def test_empty_string():
    symbols = analyze_line('""')

    assert len(symbols) == 2
    assert isinstance(symbols[0], InlineString) and symbols[0].value == ""


def test_whitespace_handling():
    assert analyze_line("does start with number a, number b, number c") == \
           analyze_line("      does   start with number a,number b,number c   ")


def test_indentation_handling():
    assert analyze_line("\t\t\t") == [LexicalIndent('\t')] * 3 + [LexicalGroupEnd(None)]


@pytest.mark.parametrize('code', UNTERMINATED_GROUPS)
def test_group_termination_errors(code):
    with pytest.raises(ValueError):
        analyze_line(code)
