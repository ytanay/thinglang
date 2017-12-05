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
    @ParserRule.predicate(lambda tokens, index: index == 0)
    def parse_access_root(left: 'BracketVector', _: LexicalAccess, right: Identifier):
        """
        Only parse [1, 2, 3].property if the BracketVector is the first token in the stream
        """
        return Access([left, right])

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: not ParserRule.is_instance(tokens[0], 'BracketVector'))
    def parse_access_predicated(left: ValueType, _: LexicalAccess, right: Identifier):
        """
        Parse the all other named access constructions
        """
        return Access([left, right])

    @staticmethod
    @ParserRule.mark
    def parse_indexed_access(target: ValueType, idx: 'BracketVector'):
        if len(idx) != 1:
            raise InvalidIndexedAccess(idx)

        return IndexedAccess(target, idx[0])
