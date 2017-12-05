from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePopDereferenced, OpcodeDereference, OpcodePushIndexImmediate, \
    OpcodePushIndex
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.errors import InvalidIndexedAccess
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.named_access import NamedAccess
from thinglang.utils.type_descriptors import ValueType


class IndexedAccess(BaseNode, ValueType):
    """
    Represents an indexed dereference.

    Examples:
        lst[0]
        hobbies[2]
     """

    def __init__(self, target, index):
        super(IndexedAccess, self).__init__([target, index])

        self.target, self.index = target, index

    def __repr__(self):
        return '{}[{}]'.format(self.target, self.index)

    def transpile(self):
        return '{}[{}]'.format(self.target.transpile(), self.index.transpile())

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
