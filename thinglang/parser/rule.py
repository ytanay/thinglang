import inspect
import itertools


class ParserRule(object):
    """
    Describes a parser rule - that is, a production rule from the thinglang grammar
    """

    COUNTER = itertools.count(0)

    def __init__(self, constructor, pattern, predicate, index=None):
        self.constructor, self.pattern, self.predicate, self.size, self.index = \
            constructor, pattern, predicate, len(pattern), (index if index is not None else next(ParserRule.COUNTER))

    def __repr__(self):
        return f'ParserRule<{self.index}>({self.pattern})'

    def matches(self, tokens):
        for start_idx, start_token in enumerate(tokens):
            token_subset = tokens[start_idx:start_idx+self.size]
            if self.does_match(token_subset) and self.predicate(*token_subset):
                return self.constructor, start_idx, start_idx + self.size

        return False

    def does_match(self, tokens):
        return len(tokens) == self.size and all(self.is_instance(token, cls) for token, cls in zip(tokens, self.pattern))

    @staticmethod
    def is_instance(inst, cls):
        if isinstance(cls, str):
            return type(inst).__name__ == cls
        elif isinstance(cls, tuple):  # To deal with mixed type/string class names
            return any(ParserRule.is_instance(inst, x) for x in cls)
        else:
            return isinstance(inst, cls)

    @staticmethod
    def mark(func, predicate=lambda *args: True):
        args = inspect.signature(func)
        func.parser_rule = ParserRule(func, [x.annotation for x in args.parameters.values()], predicate)
        return func

    @staticmethod
    def predicate(predicate):
        def wrapped(func):
            ParserRule.mark(func, predicate)
            return func
        return wrapped

