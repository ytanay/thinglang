import itertools

from thinglang.foundation import templates
from thinglang.utils import collection_utils
from thinglang.utils.mixins import ParsingMixin
from thinglang.utils.source_context import SourceReference


class BaseNode(ParsingMixin):
    STATIC = False

    def __init__(self, tokens):
        self.children = []
        self.indent = 0
        self.value = None
        self.parent = None

        self.source_ref = SourceReference.combine(collection_utils.flatten(tokens))

    def attach(self, child):
        self.children.append(child)
        child.parent = self

    def remove(self):
        """
        Remove this node from the AST
        """
        self.parent.children.remove(self)
        self.parent = None

    def tree(self, depth=1):
        separator = ('\n' if self.children else '') + ('\t' * depth)
        return '<L{}> {}({}){}{}'.format(self.source_ref.line_number if self.source_ref else "?",
                                         type(self).__name__,
                                         self,
                                         separator,
                                         separator.join(child.tree(depth=depth + 1) for child in self.children))

    @collection_utils.drain()
    def siblings_while(self, predicate):
        return itertools.takewhile(predicate, self.next_siblings())

    def next_siblings(self):
        siblings = self.parent.children
        return siblings[siblings.index(self) + 1:]

    def transpile_children(self, indent=0, children_override=None):
        sep = '\t' * indent
        return sep + ('\n' + sep).join(
            x.transpile() for x in (children_override if children_override is not None else self.children))

    def finalize(self):
        for x in self.children:
            x.finalize()

    def compile(self, context):
        for child in self.children:
            child.compile(context)

        if not self.children:
            raise Exception('Cannot pass through for further compilation')

    def deriving_from(self, node):
        self.source_ref = node.source_ref
        return self

    @property
    def container_name(self):
        from thinglang.parser.definitions.thing_definition import ThingDefinition
        node = self

        while node and not isinstance(node, ThingDefinition):
            node = node.parent

        if node and isinstance(node, ThingDefinition):
            return templates.class_names(node.name)

        raise Exception('Could not find parent container')
