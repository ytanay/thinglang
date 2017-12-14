import pytest

from tests.infrastructure.test_utils import parse_local
from thinglang.parser.errors import VectorReductionError

INVALID_SYNTAX_EXAMPLES = [
    'does 2 + 2',
    'setup returns',
    'does a returns b with number a',
    'thing SmartList with type T extends BaseList',
    'a b',
    '2 eq',
    'for',
    'number if = 1'
]

VALID_SYNTAX_EXAMPLES = [
    '2 + 2',
    'does walk',
    'a.b()',
    'f()',
    'if a'
]


@pytest.mark.parametrize('source', INVALID_SYNTAX_EXAMPLES)
def test_invalid_syntax_examples(source):
    with pytest.raises(VectorReductionError):
        parse_local(source)


@pytest.mark.parametrize('source', VALID_SYNTAX_EXAMPLES)
def test_valid_syntax_examples(source):
    parse_local(source)
