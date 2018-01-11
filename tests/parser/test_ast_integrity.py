import pytest

from tests.infrastructure.test_utils import parse_local, parse_full
from thinglang.compiler.errors import NoExceptionHandlers
from thinglang.parser.errors import StructureError

IN_THING_DEFINITION = '''
thing Person
    {}
'''.strip()

IN_METHOD_DEFINITION = '''
thing Person
    does something
        {}
    
'''

COMMON_DISALLOWED = [
    'name',
    'else',
    #'else if something eq something', TODO: reinstate
    #'handle Exception' TODO: reinstate
]

EXAMPLES = COMMON_DISALLOWED + [
    'has text name',
    'setup with text name',
    'static does something with A container returns B',
] + [
     IN_THING_DEFINITION.format(x) for x in [
        'thing Container',
        'number n = 5',
        'name',
        'for number x in numbers'
    ] + COMMON_DISALLOWED
] + [
    IN_METHOD_DEFINITION.format(x) for x in [
        'thing Container',
        'setup',
        'does gcd with number a, number b'
    ] + COMMON_DISALLOWED
]


@pytest.mark.parametrize('code', EXAMPLES)
def test_structural_integrity(code):
    with pytest.raises(StructureError) as exc:
        parse_full(code)

    print(exc.value)


def test_secondary_integrity():
    with pytest.raises(NoExceptionHandlers):
        parse_full('try')