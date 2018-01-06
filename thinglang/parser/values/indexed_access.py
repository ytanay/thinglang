from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.errors import InvalidIndexedAccess
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess
from thinglang.utils.type_descriptors import ValueType


class IndexedAccess(BaseNode, ValueType):
    """
    Represents an indexed dereference.

    Examples:
        lst[0]
     """

    def __init__(self, target, index):
        super(IndexedAccess, self).__init__([target, index])

        self.target, self.index = target, index

    def __repr__(self):
        return '{}[{}]'.format(self.target, self.index)

    def compile(self, context: CompilationBuffer):
        return MethodCall(NamedAccess.extend(self.target, Identifier('get')), ArgumentList([self.index])) \
            .deriving_from(self) \
            .compile(context)

    def assignment(self, value):
        return MethodCall(NamedAccess.extend(self.target, Identifier('set')), ArgumentList([self.index, value]),
                          is_captured=False) \
            .deriving_from(self)

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.index == other.index

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: not ParserRule.is_instance(tokens[index], 'ParenthesesVector') and
                                                (not ParserRule.is_instance(tokens[index - 1],
                                                                        LexicalAccess)) if index - 1 >= 0 else True)
    def parse_indexed_access(target: ValueType, idx: 'BracketVector'):
        if len(idx) != 1:
            raise InvalidIndexedAccess(idx)

        return IndexedAccess(target, idx[0])
