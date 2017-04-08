from thinglang.lexer.lexer import analyze_line
from thinglang.parser.symbols.base import InlineString


def test_empty_string():
    symbols = list(analyze_line('""'))

    assert len(symbols) == 2
    assert isinstance(symbols[0], InlineString) and symbols[0].value == ""
