from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.tokens.logic import LexicalBooleanTrue
from thinglang.parser.nodes.values.binary_operation import BinaryOperation
from thinglang.parser.nodes.values.inline_text import InlineString
from thinglang.parser.nodes.values.method_call import MethodCall
from thinglang.parser.nodes.blocks.conditional_else import ConditionalElse
from thinglang.parser.nodes.blocks.unconditional_else import UnconditionalElse
from thinglang.parser.nodes.blocks.conditional import Conditional


def validate_assignment(node, condition, expected_type=Conditional):
    assert node.implements(expected_type)

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
    validate_assignment(parse_local('otherwise if "dog" eq "dog"'), [InlineString, InlineString], ConditionalElse)


def test_unconditional_else():
    validate_assignment(parse_local('otherwise'), [], UnconditionalElse)
