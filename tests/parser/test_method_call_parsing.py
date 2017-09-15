from tests.infrastructure.test_utils import validate_types, parse_local
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.values.binary_operation import BinaryOperation
from thinglang.parser.nodes.values.inline_text import InlineString
from thinglang.parser.nodes.values.access import Access
from thinglang.parser.nodes.values.method_call import MethodCall


def validate_method_call(node, target, argument_types):
    assert node.implements(MethodCall)
    assert node.target == Access([LexicalIdentifier(t) for t in target])
    validate_types(node.arguments, argument_types, MethodCall, lambda x: x.arguments)


def test_simple_method_call():
    method = parse_local("person.say_hello()")
    validate_method_call(method, ['person', 'say_hello'], [])


def test_single_argument():
    method = parse_local('person.say_hello(1)')
    validate_method_call(method, ['person', 'say_hello'], [LexicalNumericalValue])


def test_multiple_inline_arguments():
    method = parse_local('person.say_hello(1, "text")')
    validate_method_call(method, ['person', 'say_hello'], [LexicalNumericalValue, InlineString])


def test_local_arguments():
    method = parse_local('person.say_hello(a, b)')
    validate_method_call(method, ['person', 'say_hello'], [LexicalIdentifier, LexicalIdentifier])


def test_simple_nested_method_calls():
    method = parse_local('person.walk(Location.random())')
    validate_method_call(method, ['person', 'walk'], [[]])


def test_nested_method_calls():
    method = parse_local('person.walk(8 * (1 + 3), Location.random(2 * (4 + 9)))')
    validate_method_call(method, ['person', 'walk'], [BinaryOperation, [BinaryOperation]])


def test_constructing_call():
    method = parse_local('create Empty(1)')
    assert method.target == Access([LexicalIdentifier('Empty'), LexicalIdentifier.constructor()])
    validate_types(method.arguments, [LexicalNumericalValue], MethodCall, lambda x: x.arguments)
    assert method.constructing_call
