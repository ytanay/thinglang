import pytest

from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.classes import MethodDefinition


def validate_method_definition(node, name, expected_arguments=(), return_type=None):
    assert node.implements(MethodDefinition)
    assert node.name == LexicalIdentifier(name)
    assert node.return_type == return_type
    for actual_argument, expected_argument in zip(node.arguments, expected_arguments):
        assert actual_argument.value == expected_argument[0]
        assert actual_argument.type.value == expected_argument[1]


def test_simple_method_definition():
    method = parse_local("does say_hello")
    validate_method_definition(method, 'say_hello')


def test_method_definition_return_type():
    method = parse_local("does compute returns number")
    validate_method_definition(method, 'compute', (), LexicalIdentifier('number'))


def test_single_argument_method_definition():
    method = parse_local("does say_hello with text message")
    validate_method_definition(method, 'say_hello', [('message', 'text')])


def test_multiple_argument_method_definition():
    method = parse_local("does say_hello with text message, number count")
    validate_method_definition(method, 'say_hello', [('message', 'text'), ('count', 'number')])


def test_combined_method_definition():
    method = parse_local("does say_hello with text message, number count returns text")
    validate_method_definition(method, 'say_hello', [('message', 'text'), ('count', 'number')], LexicalIdentifier('text'))


def test_method_definition_argument_invalid_syntax():
    with pytest.raises(ValueError):
        parse_local("does say_hello with text")

    with pytest.raises(ValueError):
        parse_local("does say_hello with text name, number")

    with pytest.raises(ValueError):
        parse_local("does say_hello with text name age")

    with pytest.raises(ValueError):
        parse_local("does say_hello with text number , , age")

    with pytest.raises(ValueError):
        parse_local("does say_hello with number, age")
