from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.method_call import MethodCall


def validate_loop(node, condition):
    assert node.implements(Loop)

    if isinstance(condition, list):
        validate_types(node.value.arguments, condition, (BinaryOperation, MethodCall), lambda x: x.arguments)
    else:
        assert isinstance(node.value, condition)


def test_simple_loop_conditionals():
    validate_loop(parse_local('while i < 5'), [LexicalIdentifier, LexicalNumericalValue])
    validate_loop(parse_local('while i < j'), [LexicalIdentifier, LexicalIdentifier])


def test_method_call_loop_conditionals():
    validate_loop(parse_local('while i < Threshold.current(1, 5)'), [LexicalIdentifier, [LexicalNumericalValue, LexicalNumericalValue]])


