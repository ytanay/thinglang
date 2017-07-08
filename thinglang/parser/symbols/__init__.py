import inspect
import itertools

import struct

from thinglang.compiler import CompilationContext
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils import tree_utils
from thinglang.utils.describable import Describable


class BaseSymbol(Describable):
    SCOPING = False
    ADVANCE = True
    EXECUTABLE = True
    SERIALIZATION = None
    STATIC = False

    def __init__(self, slice):
        self.children = []
        self.indent = 0
        self.value = None
        self.raw_slice = slice
        self.parent = None
        if slice:
            self.context = [x for x in slice if x is not None][0].context
        else:
            self.context = None

    def contextify(self, parent):
        self.parent = parent
        return self

    def populate(self, children):
        for child in children:
            child.parent = self
        self.children = children
        return self

    def attach(self, child):
        self.children.append(child)
        child.parent = self

    @tree_utils.predicated
    def find(self, predicate, single=False):
        results = []

        for child in self.children:
            results.extend(child.find(predicate))

        if predicate(self):
            results.append(self)

        if single:
            #assert len(results) == 1
            return results[0] if results else None

        return results

    @tree_utils.predicated
    def upwards(self, predicate):
        context = self
        while context:
            if predicate(context):
                return context
            context = context.parent

    def get(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def tree(self, depth=1):
        separator = ('\n' if self.children else '') + ('\t' * depth)
        return '<L{}> {}({}){}{}'.format(self.context.number if self.context else "?", type(self).__name__,
                                         self.describe(),
                                         separator,
                                         separator.join(child.tree(depth=depth + 1) for child in self.children))

    def describe(self):
        return self.value if self.value is not None else ''

    def insert_before(self, node):
        siblings = self.parent.children
        siblings.insert(siblings.index(self), node)

    def siblings_while(self, predicate):
        return itertools.takewhile(predicate, self.next_siblings())

    def next_siblings(self):
        siblings = self.parent.children
        return siblings[siblings.index(self) + 1:]

    def next_sibling(self):
        next_siblings = self.next_siblings()

        if next_siblings:
            return next_siblings[0]

    def remove(self):
        self.parent.children.remove(self)

    def references(self):
        return ()

    def statics(self):
        return ()

    def transpile(self):
        return '?{}?'.format(self)

    def transpile_children(self, indent=0, children_override=None):
        sep = '\t' * indent
        return sep + ('\n' + sep).join(x.transpile() for x in children_override or self.children)

    def serialization(self):
        return NotImplementedError('must implement serialization')

    def serialize(self):
        return struct.pack(self.SERIALIZATION, *self.serialization())

    def compile(self, context: CompilationContext):
        if self.SERIALIZATION:
            context.append(self.serialize())

        for child in self.children:
            child.compile(context)

        if not self.SERIALIZATION and not self.children:
            raise Exception('Cannot compile {}!'.format(self))


class RootSymbol(BaseSymbol):
    def __init__(self):
        super(RootSymbol, self).__init__(None)

    def compile(self, context=None):
        context = context or CompilationContext()
        super(RootSymbol, self).compile(context)
        return context

    def transpile(self):
        return self.transpile_children()

    def reorder(self):
        entry = [x for x in self.children if x.name == LexicalIdentifier("Program")]
        assert len(entry) == 1, "Program must have a single entry point - got {}".format(entry)
        self.children = sorted(self.children, key=lambda child: child.name.value)  # Secondary sort (on key)
        self.children = sorted(self.children, key=lambda child: child is not entry[0])  # Primary sort (on entry point)


class DefinitionPairSymbol(BaseSymbol):
    def __init__(self, slice):
        super(DefinitionPairSymbol, self).__init__(slice)
        self.name = slice[1]


class Transient(LexicalIdentifier):

    IDX_COUNTER = 0

    def __init__(self):
        self.idx = Transient.IDX_COUNTER
        super().__init__(self.idx)

        Transient.IDX_COUNTER += 1

    def transpile(self):
        return '__transient__{}__'.format(self.idx)

    def __str__(self):
        return 'Transient({})'.format(self.idx)

