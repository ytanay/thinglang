import itertools


from thinglang.compiler import CompilationContext
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils import collection_utils
from thinglang.utils.describable import Describable


class BaseNode(Describable):
    SCOPING = False
    ADVANCE = True
    EXECUTABLE = True
    STATIC = False

    def __init__(self, slice):
        self.children = []
        self.indent = 0
        self.value = None
        self.raw_slice = slice
        self.parent = None
        if slice and any(x is not None for x in slice): # TODO: fix this mess
            self.context = [x for x in slice if x is not None][0].context
        else:
            self.context = None

    def attach(self, child):
        self.children.append(child)
        child.parent = self

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

    def remove(self):
        self.parent.children.remove(self)

    def transpile(self):
        return '?{}?'.format(self)

    def transpile_children(self, indent=0, children_override=None):
        sep = '\t' * indent
        return sep + ('\n' + sep).join(x.transpile() for x in children_override or self.children)

    def compile(self, context: CompilationContext):
        for child in self.children:
            child.compile(context)

        if not self.children:
            raise Exception('Cannot compile {}!'.format(self))


class RootNode(BaseNode):
    def __init__(self):
        super(RootNode, self).__init__(None)

    def compile(self, context):
        super(RootNode, self).compile(context)
        return context

    def transpile(self):
        return self.transpile_children()


class DefinitionPairNode(BaseNode):
    def __init__(self, slice):
        super(DefinitionPairNode, self).__init__(slice)
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

