from tests.infrastructure.test_utils import validate_types, parse_local
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.indexed_access import IndexedAccess
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess


def validate_method_call(node, target, argument_types):
    assert isinstance(node, MethodCall)
    assert node.target == NamedAccess([Identifier(t) for t in target])
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
    method = parse_local('Empty(1)')
    assert method.target == NamedAccess([Identifier('Empty'), Identifier.constructor()])
    validate_types(method.arguments, [NumericValue], MethodCall, lambda x: x.arguments)
    assert method.constructing_call


def test_chained_call():
    call = parse_local('counter.increment().add(10)')
    validate_types(call.arguments, [NumericValue])
    assert call.target == NamedAccess([
        MethodCall(NamedAccess([
            Identifier('counter'), Identifier('increment')
        ])),
        Identifier('add')
    ])


def test_call_via_indexed_access():
    call = parse_local('a_inst[1].me()')
    assert call.target == NamedAccess([
        IndexedAccess(Identifier('a_inst'), NumericValue(1)),
        Identifier('me')
    ])
