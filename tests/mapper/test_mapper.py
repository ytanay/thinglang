from tests.mapper import SOURCE_FULL, SOURCE_PERSON, SOURCE_LOCATION, SOURCE_PAIR, get_symbols, validate_member, \
    validate_method
from thinglang.lexer.values.identifier import Identifier


def symbol_map_sanity(symbols, name, members):
    symbol_map = symbols[Identifier(name)]
    assert all(Identifier(x) in symbol_map for x in members)
    return symbol_map


def test_mapper_existence():
    symbols = get_symbols(SOURCE_FULL)
    assert all(Identifier(x) in symbols for x in ('Location', 'Pair', 'Person'))


def test_person_member_symbol_description():
    symbols = get_symbols(SOURCE_PERSON)
    person = symbol_map_sanity(symbols, 'Person', ('name', 'age', 'location', 'walk_to', 'say_hello', 'shout', 'favorite_numbers'))

    validate_member(person[Identifier('name')], Identifier('text'), 0)
    validate_member(person[Identifier('location')], Identifier('Location'), 2)


def test_location_member_symbol_description():
    symbols = get_symbols(SOURCE_LOCATION)
    symbol_map_sanity(symbols, 'Location', ('x', 'y'))


def test_pair_symbol_description():
    symbols = get_symbols(SOURCE_PAIR)
    pair = symbol_map_sanity(symbols, 'Pair', ('lhs', 'rhs', 'parts', 'nested'))

    assert pair.generics == [Identifier('T')]


def test_method_symbol_description():
    symbols = get_symbols(SOURCE_FULL)
    person, location, pair = symbols[Identifier('Person')], symbols[Identifier('Location')], symbols[Identifier('Pair')]

    validate_method(person[Identifier('walk_to')], None, ['Location'], 1)
    validate_method(location[Identifier('distance')], 'number', ['Location'] * 2, 1, True)
    validate_method(pair[Identifier('set_values')], 'T', ['T'] * 2, 1)
