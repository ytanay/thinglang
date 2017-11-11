from tests.mapper import get_symbols, SOURCE_PAIR, SOURCE_FULL, validate_member, validate_method
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier


def get_parametrized():
    pair = get_symbols(SOURCE_PAIR)[Identifier('Pair')]

    return pair.parameterize({
        Identifier('T'): Identifier('number')
    })


def test_member_parameterization():
    validate_member(get_parametrized()[Identifier('lhs')], 'number', 0)


def test_nested_member_parameterization():
    pair_number = get_parametrized()

    validate_member(pair_number[Identifier('parts')], GenericIdentifier.wrap('list', 'number'), 2)
    validate_member(pair_number[Identifier('nested')],
                    GenericIdentifier.wrap('list',
                                           GenericIdentifier.wrap('list',
                                                                  GenericIdentifier.wrap('list', 'number'))), 3)


def test_method_parameterization():
    pair_number = get_parametrized()
    validate_method(pair_number[Identifier('set_values')], 'number', ['number'] * 2, 1)
    validate_method(pair_number[Identifier('nested_param')], GenericIdentifier.wrap('list', 'number'),
                    [GenericIdentifier.wrap('list', 'number')], 2)


def test_parameterization_propagation():
    symbols = get_symbols(SOURCE_FULL)
    generic_type = symbols[Identifier('Person')][Identifier('favorite_numbers')].type
    parametrized_type = symbols[generic_type]
    assert parametrized_type.name == Identifier('Pair:<{T: number}>')
