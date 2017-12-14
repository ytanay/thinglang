from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePushIndexImmediate, OpcodePushIndex
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.errors import InvalidIndexedAccess
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
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
        ctx = self.target.compile(context)
        resolved_type = context.symbols[ctx.type][Identifier('get')]

        if isinstance(self.index, NumericValue):
            context.append(OpcodePushIndexImmediate(self.index.value), self.source_ref)
        else:
            self.index.compile(context)
            context.append(OpcodePushIndex(), self.source_ref)

        return resolved_type

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.index == other.index

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: not ParserRule.is_instance(tokens[0], 'ParenthesesVector'))
    def parse_indexed_access(target: ValueType, idx: 'BracketVector'):
        if len(idx) != 1:
            raise InvalidIndexedAccess(idx)

        return IndexedAccess(target, idx[0])

