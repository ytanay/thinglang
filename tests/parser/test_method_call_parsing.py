from tests.infrastructure.test_utils import validate_types, parse_local
from thinglang.lexer.values.numeric import NumericValue
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.values.access import Access
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.method_call import MethodCall


def validate_method_call(node, target, argument_types):
    assert node.implements(MethodCall)
    assert node.target == Access([Identifier(t) for t in target])
    validate_types(node.arguments, argument_types, MethodCall, lambda x: x.arguments)


def test_simple_method_call():
    method = parse_local("person.say_hello()")
    validate_method_call(method, ['person', 'say_hello'], [])


def test_single_argument():
    method = parse_local('person.say_hello(1)')
    validate_method_call(method, ['person', 'say_hello'], [NumericValue])


def test_multiple_inline_arguments():
    method = parse_local('person.say_hello(1, "text")')
    from thinglang.parser.values.inline_text import InlineString
    validate_method_call(method, ['person', 'say_hello'], [NumericValue, InlineString])


def test_local_arguments():
    method = parse_local('person.say_hello(a, b)')
    validate_method_call(method, ['person', 'say_hello'], [Identifier, Identifier])


def test_simple_nested_method_calls():
    method = parse_local('person.walk(Location.random())')
    validate_method_call(method, ['person', 'walk'], [[]])


def test_nested_method_calls():
    method = parse_local('person.walk(8 * (1 + 3), Location.random(2 * (4 + 9)))')
    validate_method_call(method, ['person', 'walk'], [BinaryOperation, [BinaryOperation]])


def test_constructing_call():
    method = parse_local('create Empty(1)')
    assert method.target == Access([Identifier('Empty'), Identifier.constructor()])
    validate_types(method.arguments, [NumericValue], MethodCall, lambda x: x.arguments)
    assert method.constructing_call
