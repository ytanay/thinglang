import copy

from thinglang.lexer.values.identifier import Identifier


class LocalTracker(object):
    TRACKER_SENTINEL = object()

    def __init__(self, type: Identifier):
        self.type = type
        self.hits = 0

    def hit(self):
        self.hits += 1

    @property
    def index(self):
        return self.TRACKER_SENTINEL

    def __repr__(self):
        return f'Tracker({self.type}: {self.hits})'


class TrackedReplacements(object):

    def __init__(self, argument_names, argument_values):
        self.replacements = {name: value for name, value in zip(argument_names, argument_values)}

    def __getitem__(self, item):
        assert isinstance(item, Identifier)

        if item not in self.replacements:
            return item

        return copy.deepcopy(self.replacements[item]).deriving_from(item)


class ResolvableIndex(object):

    def __init__(self, index=None):
        super().__init__()
        self.index = index

    def __add__(self, other):
        return self.index + other
