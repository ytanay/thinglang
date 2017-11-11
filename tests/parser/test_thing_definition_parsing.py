from tests.infrastructure.test_utils import parse_local
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.thing_definition import ThingDefinition


def validate_thing_definition(node, name, extends=None, generics=None):
    assert isinstance(node, ThingDefinition)
    assert node.name == (name if isinstance(name, Identifier) else Identifier(name))
    assert node.extends == (Identifier(extends) if extends else None)
    assert node.generics == ([Identifier(x) for x in generics] if generics else None)


def test_simple_thing_definition():
    method = parse_local('thing Person')
    validate_thing_definition(method, 'Person')


def test_thing_definition_inheritance():
    method = parse_local('thing Child extends Person')
    validate_thing_definition(method, 'Child', 'Person')


def test_thing_definition_generic():
    node = parse_local('thing SmartList with type T')
    validate_thing_definition(node, 'SmartList', generics=['T'])

    node = parse_local('thing SmartList with type T, type V')
    validate_thing_definition(node, 'SmartList', generics=['T', 'V'])


def test_thing_definition_inheritance_and_generic():
    node = parse_local('thing SmartList extends BaseList with type T, type V')
    validate_thing_definition(node, 'SmartList', 'BaseList', ['T', 'V'])
