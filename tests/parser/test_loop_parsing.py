from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.blocks.iteration_loop import IterationLoop
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.method_call import MethodCall


def validate_loop(node, condition):
    assert isinstance(node, Loop)

    if isinstance(condition, list):
        validate_types(node.value.arguments, condition, (BinaryOperation, MethodCall), lambda x: x.arguments)
    else:
        assert isinstance(node.value, condition)


def test_simple_loop_conditionals():
    validate_loop(parse_local('while i < 5'), [Identifier, NumericValue])
    validate_loop(parse_local('while i < j'), [Identifier, Identifier])


def test_method_call_loop_conditionals():
    validate_loop(parse_local('while i < Threshold.current(1, 5)'), [Identifier, [NumericValue, NumericValue]])


def test_iteration_loop_parsing():
    loop = parse_local('for number n in numbers')

    assert isinstance(loop, IterationLoop)
    assert loop.target == Identifier('n')
    assert loop.target_type == Identifier('number')
    assert loop.collection == Identifier('numbers')

