from tests.mapper import SOURCE_FULL, SOURCE_PERSON, SOURCE_LOCATION, SOURCE_PAIR, get_symbols
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.symbol import Symbol


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

    name_desc = person[Identifier('name')]

    assert name_desc.kind is Symbol.MEMBER
    assert name_desc.type == Identifier('text')
    assert name_desc.visibility is Symbol.PUBLIC
    assert not name_desc.static
    assert name_desc.index == 0

    location_desc = person[Identifier('location')]
    assert location_desc.kind is Symbol.MEMBER
    assert location_desc.type == Identifier('Location')
    assert location_desc.visibility is Symbol.PUBLIC
    assert not location_desc.static
    assert location_desc.index == 2


def test_location_member_symbol_description():
    symbols = get_symbols(SOURCE_LOCATION)
    symbol_map_sanity(symbols, 'Location', ('x', 'y'))


def test_pair_symbol_description():
    symbols = get_symbols(SOURCE_PAIR)
    pair = symbol_map_sanity(symbols, 'Pair', ('lhs', 'rhs'))

    assert pair.generics == [Identifier('T')]


def test_method_symbol_description():
    symbols = get_symbols(SOURCE_FULL)
    person, location, pair = symbols[Identifier('Person')], symbols[Identifier('Location')], symbols[Identifier('Pair')]

    walk_to = person[Identifier('walk_to')]
    assert walk_to.kind is Symbol.METHOD
    assert walk_to.type is None
    assert walk_to.arguments == [Identifier('Location')]
    assert not walk_to.static

    distance = location[Identifier('distance')]
    assert distance.kind is Symbol.METHOD
    assert distance.type == Identifier('number')
    assert distance.arguments == [Identifier('Location')] * 2
    assert distance.static

    set_values = pair[Identifier('set_values')]
    assert set_values.kind is Symbol.METHOD
    assert set_values.type == Identifier('T')
    assert set_values.arguments == [Identifier('T')] * 2
    assert not set_values.static
