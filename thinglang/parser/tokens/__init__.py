from thinglang.utils.describable import Describable


class BaseToken(Describable):
    BLOCK = False
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

    def find(self, predicate):
        results = []

        for child in self.children:
            results.extend(child.find(predicate))

            if predicate(child):
                results.append(child)

        if predicate(self):
            results.append(self)

        return results

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


class RootToken(BaseToken):
    BLOCK = True

    def __init__(self):
        super(RootToken, self).__init__(None)


class DefinitionPairToken(BaseToken):
    def __init__(self, slice):
        super(DefinitionPairToken, self).__init__(slice)
        self.name = slice[1].value


class Transient(object):

    IDX_COUNTER = -1

    def __init__(self):
        self.idx = Transient.IDX_COUNTER
        Transient.IDX_COUNTER += 1

    def __str__(self):
        return 'Transient({})'.format(self.idx)
