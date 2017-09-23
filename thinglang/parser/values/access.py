from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodePopDereferenced, OpcodeDereference
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class Access(BaseNode, ValueType):
    def __init__(self, target):
        super(Access, self).__init__(target)

        self.target = target
        self.type = None
        self.arguments = []

    def describe(self):
        return '{}:{}'.format('.'.join(str(x) for x in self.target), self.type)

    def transpile(self):
            return '->'.join(x.transpile() for x in self.target)

    def compile(self, context: CompilationContext, pop_last=False, without_last=False):

        if without_last and not self.extensions:
            return self[0].compile(context)

        ref = context.push_ref(context.resolve(self.root), self.source_ref)

        for ext, last in self.extensions:
            if last and without_last:
                break

            ref = context.symbols.dereference(ref.element, ext)
            cls = OpcodePopDereferenced if pop_last and last else OpcodeDereference
            context.append(cls(ref.element_index), self.source_ref)

        return ref

    @property
    def root(self):
        return Access(self.target[:2])

    @property
    def extensions(self):
        last = self.target[-1]
        return [(x, x is last) for x in self.target[2:]]

    def __getitem__(self, item):
        return self.target[item]

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target

    def __len__(self):
        size = len(self.target)
        assert size >= 2
        return size

    @staticmethod
    @ParserRule.mark
    def parse_access_chain(root: 'Access', _: LexicalAccess, extension: Identifier):
        return Access(root.target + [extension])

    @staticmethod
    @ParserRule.mark
    def parse_access_start(left: Identifier, _: LexicalAccess, right: Identifier):
        return Access([left, right])

