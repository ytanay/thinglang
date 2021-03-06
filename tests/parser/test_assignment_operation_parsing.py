from tests.infrastructure.test_utils import parse_local
from tests.parser.test_method_call_parsing import validate_method_call
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.inline_text import InlineString
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.method_call import MethodCall


def validate_assignment(node, type, name, value):
    assert isinstance(node, AssignmentOperation)
    assert node.name == Identifier(name)
    assert node.name.type == (Identifier(type) if type else None)
    assert node.intent == (AssignmentOperation.DECELERATION if type else AssignmentOperation.REASSIGNMENT)

    if value in (MethodCall, BinaryOperation):
        assert isinstance(node.value, value)


def test_immediate_declarations():
    validate_assignment(parse_local('number a = 5'), 'number', 'a', NumericValue(5))
    validate_assignment(parse_local('text a = "hello world!"'), 'text', 'a', InlineString('hello world!'))


def test_immediate_assignments():
    validate_assignment(parse_local('a = 5'), None, 'a', NumericValue(5))
    validate_assignment(parse_local('a = "hello world!"'), None, 'a', InlineString('hello world!'))


def test_simple_method_call_value_type():
    assignment = parse_local('number a = number.random()')
    validate_assignment(assignment, 'number', 'a', MethodCall)
    validate_method_call(assignment.value, ['number', 'random'], [])


def test_complex_method_call_value_type():
    assignment = parse_local('number a = distribution.normal(number.random(10), number.random(25))')
    validate_assignment(assignment, 'number', 'a', MethodCall)
    validate_method_call(assignment.value, ['distribution', 'normal'], [[NumericValue], [NumericValue]])


def test_arithmetic_operation_value_type():
    assignment = parse_local('number a = 2 * (4 + 2) * (3 + 2)')
    validate_assignment(assignment, 'number', 'a', BinaryOperation)
    assert assignment.value.evaluate() == 60


def test_in_place_modifier():
    reassignment = parse_local('a += 2 * 8')
    validate_assignment(reassignment, None, 'a', BinaryOperation)
    assert reassignment.value.lhs == Identifier('a')
    assert isinstance(reassignment.value.rhs, BinaryOperation)
    assert reassignment.value.rhs.evaluate() == 16
