from tests.infrastructure.test_utils import parse_local
from thinglang.lexer.values.identifier import GenericIdentifier, Identifier
from thinglang.parser.statements.assignment_operation import AssignmentOperation


def test_generic_parsing():
    node = parse_local('list<number> l = [1, 2, 3]')

    assert isinstance(node, AssignmentOperation)
    assert isinstance(node.name, Identifier)
    assert isinstance(node.name.type, GenericIdentifier)
    assert node.name == Identifier('l')
    assert node.name.type.value == Identifier('list')
    assert node.name.type.generics == (Identifier('number'),)


