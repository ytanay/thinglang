from thinglang.parser.errors import UnresolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.functions import Access


class Resolver(object):

    UNRESOLVED_REFERENCE = object()

    def __init__(self, stack, heap):
        self.stack, self.heap = stack, heap

    def resolve(self, identifier):
        return self.validate(identifier, self.lookup(identifier))

    def lookup(self, identifier):
        if isinstance(identifier, LexicalIdentifier):
            if identifier in self.stack:
                return self.stack[identifier]

            if identifier in self.heap:
                return self.heap[identifier]

            return self.UNRESOLVED_REFERENCE

        if identifier[0].is_self():
            return self.search(identifier[1:], self.stack.instance)

        stack_value = self.search(identifier, self.stack)
        if stack_value is not self.UNRESOLVED_REFERENCE:
            return stack_value

        return self.search(identifier, self.heap)

    @classmethod
    def search(cls, identifier, context):
        for component in identifier:
            if component not in context:
                return cls.UNRESOLVED_REFERENCE

            context = context[component]

        return context

    def validate(self, identifier, value):
        if value is self.UNRESOLVED_REFERENCE:
            raise UnresolvedReference(f'Cannot find reference {identifier} in stack={self.stack}, heap={self.heap}')
        return value

    def set(self, key, value):
        if isinstance(key, Access):
            container = self.resolve(key[:-1])
            container[key[-1]] = value
        else:
            self.stack[key] = value
