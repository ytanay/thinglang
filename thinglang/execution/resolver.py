from thinglang.execution.errors import UnknownVariable
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols.functions import Access

UNRESOLVABLE_REFERENCE = object()


class Resolver(object):

    def __init__(self, stack, heap):
        self.stack, self.heap = stack, heap

    def resolve(self, identifier):
        if isinstance(identifier, LexicalIdentifier):
            if identifier in self.stack:
                return self.stack[identifier]

            if identifier in self.heap:
                return self.heap[identifier]

            self.validate(identifier, UNRESOLVABLE_REFERENCE)

        if identifier[0].is_self():
            return self.validate(identifier, self.search(identifier[1:], self.stack.instance))

        stack_value = self.search(identifier, self.stack)
        if stack_value is not UNRESOLVABLE_REFERENCE:
            return stack_value

        return self.validate(identifier, self.search(identifier, self.heap))

    @staticmethod
    def search(identifier, context):
        for component in identifier:
            if component not in context:
                return UNRESOLVABLE_REFERENCE

            context = context[component]

        return context

    def validate(self, identifier, value):
        if value is UNRESOLVABLE_REFERENCE:
            raise UnknownVariable(f'Cannot find reference {identifier} in stack={self.stack}, heap={self.heap}')
        return value

    def set(self, key, value):
        if isinstance(key, Access):
            container = self.resolve(key[:-1])
            container[key[-1]] = value
        else:
            self.stack[key] = value
