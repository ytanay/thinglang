from tests.infrastructure.test_utils import parse_local
from thinglang.lexer.values.identifier import GenericIdentifier, Identifier
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.statements.assignment_operation import AssignmentOperation



def test_generic_parsing():
    node = parse_local('list<number> l = [1, 2, 3]')

    assert isinstance(node, AssignmentOperation)
    assert isinstance(node.name, Identifier)
    assert isinstance(node.name.type, GenericIdentifier)
    assert node.name == Identifier('l')
    assert node.name.type.name == Identifier('list')
    assert node.name.type.generic == Identifier('number')


def test_generic_class_description():
    node = parse_local('thing SmartList with type T')

    assert isinstance(node, ThingDefinition)
    assert node.name == Identifier('SmartList')
    print(node.generics[0].type)
    assert node.generics[0] == Identifier('T')