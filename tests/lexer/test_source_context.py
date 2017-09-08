from tests.infrastructure.test_utils import lexer_single


def test_source_reference_lexical_output():
    code = "does start with number a, number b = 42"
    tokens = lexer_single(code, without_end=True)

    assert [code[token.source_ref.column_start:token.source_ref.column_end] for token in tokens] == \
           ['does', 'start', 'with', 'number', 'a', ',', 'number', 'b', '=', '42']