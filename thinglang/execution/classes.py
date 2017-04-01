from thinglang.lexer.tokens.base import LexicalIdentifier


class ThingInstance(object):

    def __init__(self, cls):
        self.cls = cls
        self.methods = {
            x.name: x for x in self.cls.children
        }
        self.members = {}

    def __contains__(self, item):
        return item in self.members or item in self.methods

    def __getitem__(self, item):
        return self.members.get(item) if item in self.members else self.methods[item]

    def __setitem__(self, key, value):
        assert isinstance(key, LexicalIdentifier)
        self.members[key] = value

    def __str__(self):
        return f'Thing<{self.cls}>(members={self.members}, methods={self.methods})'
