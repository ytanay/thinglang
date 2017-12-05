from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.errors import InvalidIndexedAccess
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.access import Access
from thinglang.parser.values.indexed_access import IndexedAccess
from thinglang.utils.type_descriptors import ValueType


class UniversalAccess(BaseNode):
    """
    Parses named and indexed dereference operations in a correct order
    """

    def __init__(self):
        raise NotImplemented('Do not instantiate a UniversalAccess object')

    @staticmethod
    @ParserRule.mark
    def parse_access_chain(root: Access, _: LexicalAccess, extension: Identifier):
        return Access(root.target + [extension])

    @staticmethod
    @ParserRule.predicate(lambda left, _, right: not ParserRule.is_instance(left, 'BracketVector'))
    def parse_access_predicated(left: ValueType, _: LexicalAccess, right: Identifier):
        return Access([left, right])

    @staticmethod
    @ParserRule.mark
    def parse_indexed_access(target: ValueType, idx: 'BracketVector'):
        if len(idx) != 1:
            raise InvalidIndexedAccess(idx)

        return IndexedAccess(target, idx[0])

    @staticmethod
    @ParserRule.mark
    def parse_access_root(left: ValueType, _: LexicalAccess, right: Identifier):
        return Access([left, right])
