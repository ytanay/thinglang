import itertools

from thinglang.foundation import templates
from thinglang.utils import collection_utils
from thinglang.utils.mixins import ParsingMixin
from thinglang.utils.source_context import SourceReference


class BaseNode(ParsingMixin):
    """
    The base AST node
    """

    STATIC = False

    def __init__(self, tokens):
        self.children = []
        self.indent = 0
        self.value = None
        self.parent = None

        self.source_ref = SourceReference.combine(collection_utils.flatten(tokens))

    def attach(self, child):
        """
        Attach a child to this node
        """
        self.children.append(child)
        child.parent = self

    def remove(self):
        """
        Remove this node from the AST
        """
        self.parent.children.remove(self)
        self.parent = None

    def next_siblings(self):
        """
        Returns this node's siblings, starting after this node
        :return:
        """
        siblings = self.parent.children
        return siblings[siblings.index(self) + 1:]

    @collection_utils.drain()
    def siblings_while(self, predicate):
        """
        Emits this node's siblings (starting after the node) until predicate returns true
        """
        return itertools.takewhile(predicate, self.next_siblings())

    def transpile_children(self, indent=0, children_override=None):
        """
        Calls the transpile method on this node and its siblings
        """
        sep = '\t' * indent
        return sep + ('\n' + sep).join(
            x.transpile() for x in (children_override if children_override is not None else self.children))

    def finalize(self):
        """
        Calls the finalize method on this nodes siblings
        """
        for x in self.children:
            x.finalize()

    def compile(self, context):
        """
        Recursively compile this nodes children
        """
        for child in self.children:
            child.compile(context)

        if not self.children:
            raise Exception('Cannot pass through for further compilation')

    def deriving_from(self, node):
        """
        Override the source reference for this node by providing the source node
        """
        self.source_ref = node.source_ref
        return self

    def walk_up(self, predicate):
        """
        Walk up the AST until predicate returns True, returning the first matching node, or None if no matches
        are found.
        """
        node = self

        while node and not predicate(node):
            node = node.parent

        if node and predicate(node):
            return node

    @property
    def container_name(self):
        """
        Walk up the AST to find the class names for the enclosing ThingDefinition of this node
        """
        from thinglang.parser.definitions.thing_definition import ThingDefinition
        thing_definition = self.walk_up(lambda x: isinstance(x, ThingDefinition))
        return templates.class_names(thing_definition.name)

    @property
    def enclosing_method(self):
        """
        Walk up the AST to find the enclosing MethodDefinition for this node
        """
        from thinglang.parser.definitions.method_definition import MethodDefinition
        return self.walk_up(lambda x: isinstance(x, MethodDefinition))

    def tree(self, depth=1):
        """
        Prints this node and its children in a tree-like format
        """
        separator = ('\n' if self.children else '') + ('\t' * depth)
        return '<L{}> {}({}){}{}'.format(self.source_ref.line_number if self.source_ref else "?",
                                         type(self).__name__,
                                         self,
                                         separator,
                                         separator.join(child.tree(depth=depth + 1) for child in self.children))
