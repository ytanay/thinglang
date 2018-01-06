import collections

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePopDereferenced, OpcodeDereference
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType

ExtensionInfo = collections.namedtuple('ExtensionInfo', ['value', 'is_last'])


class NamedAccess(BaseNode, ValueType):
    """
    Represents a named dereference operation.
    Examples:
        person.walk
        person.info.age
    """

    def __init__(self, target, tokens=None):
        super(NamedAccess, self).__init__(target if tokens is None else tokens)

        self.target = target
        self.type = None

    def __repr__(self):
        return '{}'.format('.'.join(str(x) for x in self.target))

    def compile(self, context: CompilationBuffer, pop_last=False, without_last=False):
        """
        Compiling NamedAccess objects involves compiling each component in turn, maintaining the last generated reference.
        :param context:
        We start with the root (an order-2 tuple)
            If the root is a pure Identifier pair, resolve the pair and emit a PushMember opcode
            Otherwise, compile the first component, and emit a Dereference opcode for the second
        :param pop_last:
        :param without_last:
        :return:
        """
        assert len(self) >= 2

        if without_last and not self.extensions:
            return self[0].compile(context)

        extensions = self.extensions

        if isinstance(self[0], Identifier):
            assert isinstance(self[1], Identifier)
            ref = context.push_ref(context.resolve(self.root), self.source_ref)
        else:
            ref = self[0].compile(context)
            extensions = [ExtensionInfo(self[1], len(self) == 2)] + extensions

        for ext, last in extensions:
            if last and without_last:
                break

            ref = context.resolve(NamedAccess([ref.type, ext], tokens=self))
            cls = OpcodePopDereferenced if pop_last and last else OpcodeDereference
            context.append(cls(ref.element_index), self.source_ref)

        return ref

    @property
    def root(self):
        return NamedAccess(self.target[:2])

    @property
    def extensions(self):
        last = self.target[-1]
        return [ExtensionInfo(x, x is last) for x in self.target[2:]]

    @property
    def is_identifier_pair(self):
        return not self.extensions and all(isinstance(x, Identifier) for x in self)

    def __getitem__(self, item):
        return self.target[item]

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target

    def __len__(self):
        size = len(self.target)
        assert size >= 2
        return size

    def append(self, other):
        self.target.append(other)
        return self

    def deriving_from(self, node):
        for arg in self.target:
            arg.deriving_from(node)

        return super().deriving_from(node)

    @classmethod
    def extend(cls, base, extension: Identifier) -> 'NamedAccess':
        if isinstance(base, NamedAccess):
            return NamedAccess(base.target + [extension])

        return NamedAccess([base, extension])

    @staticmethod
    @ParserRule.mark
    def parse_access_chain(root: 'NamedAccess', _: LexicalAccess, extension: Identifier):
        return NamedAccess(root.target + [extension])

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: index == 0)
    def parse_access_root(left: 'BracketVector', _: LexicalAccess, right: Identifier):
        """
        Only parse [1, 2, 3].property if the BracketVector is the first token in the stream
        """
        return NamedAccess([left, right])

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: not ParserRule.is_instance(tokens[index], ('BracketVector', 'ParenthesesVector')))
    def parse_access_predicated(left: ValueType, _: LexicalAccess, right: Identifier):
        """
        Parse the all other named access constructions
        """
        return NamedAccess([left, right])

    @classmethod
    def auto(cls, param):
        return NamedAccess([Identifier(x) for x in param.split('.')])
