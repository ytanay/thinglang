from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePopDereferenced, OpcodeDereference
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.errors import InvalidIndexedAccess
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.access import Access
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

    def compile(self, context: CompilationBuffer, pop_last=False, without_last=False):
        if without_last and not self.extensions:
            return self[0].compile(context)

        ref = context.push_ref(context.resolve(self.root), self.source_ref)

        for ext, last in self.extensions:
            if last and without_last:
                break

            ref = context.symbols.resolve_partial(ref, ext)
            cls = OpcodePopDereferenced if pop_last and last else OpcodeDereference
            context.append(cls(ref.element_index), self.source_ref)

        return ref

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target and self.index == other.index
