from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.values.booleans import LexicalBooleanTrue
from thinglang.lexer.values.inline_text import InlineString
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.conditional_else import ConditionalElse
from thinglang.parser.blocks.unconditional_else import UnconditionalElse
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.method_call import MethodCall


def validate_assignment(node, condition, expected_type=Conditional):
    assert isinstance(node, expected_type)

    if expected_type is UnconditionalElse:
        return

    if isinstance(condition, list):
        validate_types(node.value.arguments, condition, (BinaryOperation, MethodCall), lambda x: x.arguments)
    else:
        assert isinstance(node.value, condition)


def test_boolean_primitive_conditional():
    validate_assignment(parse_local('if true'), LexicalBooleanTrue)


def test_simple_equality():
    validate_assignment(parse_local('if "dog" eq "dog"'), [InlineString, InlineString])


def test_equality_method_call():
        validate_assignment(parse_local('if "dog" eq DogFactory.build_dog("german_shepherd")'), [InlineString, [InlineString]])


def test_conditional_else():
    validate_assignment(parse_local('else if "dog" eq "dog"'), [InlineString, InlineString], ConditionalElse)


def test_unconditional_else():
    validate_assignment(parse_local('else'), [], UnconditionalElse)
