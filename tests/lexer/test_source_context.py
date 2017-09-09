from tests.infrastructure.test_utils import lexer_single, parse_local


def test_source_reference_lexical_output():
    code = "does start with number a, number b = 42"
    tokens = lexer_single(code, without_end=True)

    assert [code[token.source_ref.column_start:token.source_ref.column_end] for token in tokens] == \
           ['does', 'start', 'with', 'number', 'a', ',', 'number', 'b', '=', '42']


def test_source_reference_parser_output():
    ast = parse_local('number a = distribution.normal(number.random(10), number.random(25))')

    assignment_name, outer_function_target, inner_function_argument = \
        ast.name.source_ref, ast.value.target.source_ref, ast.value.arguments[1].arguments[0].source_ref

    assert assignment_name.column_start == 7 and assignment_name.column_end == 8
    assert outer_function_target.column_start == 11 and outer_function_target.column_end == 30
    assert inner_function_argument.column_start == 64 and inner_function_argument.column_end == 66

