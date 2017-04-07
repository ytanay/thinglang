import inspect

from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils import tree_utils
from thinglang.utils.describable import Describable


class BaseSymbol(Describable):
    SCOPING = False
    ADVANCE = True

    def __init__(self, slice):
        self.children = []
        self.indent = 0
        self.value = None
        self.raw_slice = slice
        self.parent = None
        if slice:
            self.context = slice[-1].context
        else:
            self.context = None

    def contextify(self, parent):
        self.parent = parent
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

    def references(self):
        return ()


class RootSymbol(BaseSymbol):
    def __init__(self):
        super(RootSymbol, self).__init__(None)


class DefinitionPairSymbol(BaseSymbol):
    def __init__(self, slice):
        super(DefinitionPairSymbol, self).__init__(slice)
        self.name = slice[1]


class Transient(LexicalIdentifier):

    IDX_COUNTER = -1

    def __init__(self):
        self.idx = Transient.IDX_COUNTER
        super().__init__(self.idx)

        Transient.IDX_COUNTER += 1

    def __str__(self):
        return 'Transient({})'.format(self.idx)

