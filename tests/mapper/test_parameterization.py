from tests.mapper import get_symbols, SOURCE_PAIR, SOURCE_FULL
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.symbol import Symbol


def test_simple_parameterization():
    pair = get_symbols(SOURCE_PAIR)[Identifier('Pair')]

    pair_number = pair.parameterize({
        Identifier('T'): Identifier('number')
    })

    lhs_desc = pair_number[Identifier('lhs')]
    assert lhs_desc.kind is Symbol.MEMBER
    assert lhs_desc.type == Identifier('number')
    assert lhs_desc.visibility is Symbol.PUBLIC
    assert not lhs_desc.static
    assert lhs_desc.index == 0

    set_values = pair_number[Identifier('set_values')]
    assert set_values.kind is Symbol.METHOD
    assert set_values.type == Identifier('number')
    assert set_values.visibility is Symbol.PUBLIC
    assert not set_values.static
    assert set_values.index == 1
    assert set_values.arguments == [Identifier('number')] * 2

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
