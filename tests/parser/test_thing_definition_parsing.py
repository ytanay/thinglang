from tests.infrastructure.test_utils import parse_local
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.thing_definition import ThingDefinition


def validate_thing_definition(node, name, extends=None):
    assert node.implements(ThingDefinition)
    assert node.name == (name if isinstance(name, Identifier) else Identifier(name))
    assert node.extends == (Identifier(extends) if extends else None)


def test_simple_thing_definition():
    method = parse_local('thing Person')
    validate_thing_definition(method, 'Person')


def test_thing_definition_inheritance():
    method = parse_local('thing Child extends Person')
    validate_thing_definition(method, 'Child', 'Person')


