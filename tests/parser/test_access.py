from tests.infrastructure.test_utils import parse_local, normalize_id
from tests.parser.test_method_call_parsing import validate_method_call
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.values.access import Access
from thinglang.parser.values.indexed_access import IndexedAccess
from thinglang.parser.values.inline_list import InlineList
from thinglang.parser.values.method_call import MethodCall


def validate_indexed_access(node, target, index):
    assert isinstance(node, IndexedAccess)
    assert node.target == normalize_id(target)
    assert node.index == normalize_id(index)


def validate_access(node, target):
    assert isinstance(node, Access)
    assert node.target == normalize_id(target)


def test_simple_access():
    validate_access(parse_local('a.b'), ['a', 'b'])


def test_chained_access():
    validate_access(parse_local('a.b.c.d'), ['a', 'b', 'c', 'd'])


def test_local_index_access():
    validate_indexed_access(parse_local('a[0]'), 'a', NumericValue(0))


def test_member_index_access():
    validate_indexed_access(parse_local('person.hobbies[idx]'),
                            Access([Identifier('person'), Identifier('hobbies')]),
                            'idx')


def test_chained_index_access():
    validate_indexed_access(parse_local('person.hobbies[idx]'),
                            Access([Identifier('person'), Identifier('hobbies')]),
                            'idx')

    validate_indexed_access(parse_local('game.map[x][y]'),
                            IndexedAccess(Access([Identifier('game'), Identifier('map')]), Identifier('x')),
                            'y')


def test_complex_mixed_access():

    node = parse_local('person.hobbies.all[selection.index].effects[selection.effect()]')

    assert isinstance(node, IndexedAccess)
    assert isinstance(node.target, Access)

    validate_method_call(node.index, ['selection', 'effect'], [])
    assert node.target == Access([
        IndexedAccess(
            Access([Identifier('person'), Identifier('hobbies'), Identifier('all')]),
            Access([Identifier('selection'), Identifier('index')])),
        Identifier('effects')
        ])

    node = parse_local('person.hobbies.generate()[selection.index].effects[selection.effect()]')

    assert isinstance(node, IndexedAccess)
    assert isinstance(node.target, Access)

    validate_method_call(node.index, ['selection', 'effect'], [])
    assert node.target == Access([
        IndexedAccess(
            MethodCall(Access([Identifier('person'), Identifier('hobbies'), Identifier('generate')])),
            Access([Identifier('selection'), Identifier('index')])),
        Identifier('effects')
    ])


def test_complex_mixed_access_ambiguity():
    node = parse_local('person.hobbies.generate(123, [selection.index].effects[selection.effect()])')

    assert isinstance(node, MethodCall)
    assert node.target == Access([Identifier('person'), Identifier('hobbies'), Identifier('generate')])
    assert len(node.arguments) == 2
    assert node.arguments[0] == NumericValue(123)
    assert node.arguments[1] == IndexedAccess(
        Access([
            InlineList(Access([Identifier('selection'), Identifier('index')])),
            Identifier('effects')]),
        MethodCall(Access([Identifier('selection'), Identifier('effect')]))
    )
