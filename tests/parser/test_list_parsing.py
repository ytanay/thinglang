from tests.infrastructure.test_utils import parse_local, validate_types
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.values.inline_list import InlineList
from thinglang.parser.values.inline_text import InlineString
from thinglang.parser.values.method_call import MethodCall


def validate_list(node, types):
    assert node.implements(InlineList)

    validate_types(node.values, types, InlineList, lambda x: x.values)


def test_simple_inline_list():
    validate_list(parse_local('[1, 2, 3]'), [NumericValue] * 3)
    validate_list(parse_local('[1, "text", 3]'), [NumericValue, InlineString, NumericValue])


def test_inline_list_assignment():
    validate_list(parse_local('number b = [[1, 2], a.b(), "hi"]').value, [[NumericValue] * 2, MethodCall, InlineString])


def test_empty_inline_list():
    validate_list(parse_local('[]'), [])

