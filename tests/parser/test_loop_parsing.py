from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.functions import MethodCall
from thinglang.parser.nodes.logic import Loop


def validate_loop(node, condition):
    assert node.implements(Loop)

    if isinstance(condition, list):
        validate_types(node.condition.arguments, condition, (ArithmeticOperation, MethodCall), lambda x: x.arguments)
    else:
        assert isinstance(node.value, condition)


def test_simple_loop_conditionals():
    validate_loop(parse_local('repeat while i < 5'), [LexicalIdentifier, LexicalNumericalValue])
    validate_loop(parse_local('repeat while i < j'), [LexicalIdentifier, LexicalIdentifier])


def test_method_call_loop_conditionals():
    validate_loop(parse_local('repeat while i < Threshold.current(1, 5)'), [LexicalIdentifier, [LexicalNumericalValue, LexicalNumericalValue]])


