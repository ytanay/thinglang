import inspect
import itertools


class ParserRule(object):
    COUNTER = itertools.count(0)

    def __init__(self, constructor, pattern, index=None):
        self.constructor, self.pattern, self.size, self.index = constructor, pattern, len(pattern), (index if index is not None else next(ParserRule.COUNTER))

    def __repr__(self):
        return f'ParserRule<{self.index}>({self.pattern})'

    def matches(self, tokens):
        for start_idx, start_token in enumerate(tokens):

            if self.does_match(tokens[start_idx:start_idx+self.size]):
                return self.constructor, start_idx, start_idx + self.size

        return False

    def does_match(self, tokens):
        return len(tokens) == self.size and all(self.is_instance(token, cls) for token, cls in zip(tokens, self.pattern))

    @staticmethod
    def is_instance(inst, cls):
        if isinstance(cls, str):
            return type(inst).__name__ == cls

        return isinstance(inst, cls)

    @staticmethod
    def mark(func):
        args = inspect.signature(func)
        func.parser_rule = ParserRule(func, [x.annotation for x in args.parameters.values()])
        return func
