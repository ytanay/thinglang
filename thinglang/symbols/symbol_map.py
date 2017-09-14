from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.symbols.symbol import Symbol


class SymbolMap(object):

    def __init__(self, members: list, methods: list, name: LexicalIdentifier, index: int):
        self.members, self.methods, self.name, self.index = members, methods, name, index

        self.lookup = {
            elem.name: elem for elem in (self.methods + self.members)
        }

        assert len(self.methods) + len(self.members) == len(self.lookup), 'Thing definition contains colliding elements'

    def override_index(self, new_index):
        self.index = new_index

    def serialize(self):
        return {
            "name": self.name,
            "index": self.index,
            "symbols": [x.serialize() for x in self.lookup.values()]
        }

    @classmethod
    def from_serialized(cls, data: dict):
        symbols = [Symbol.load(elem) for elem in data['symbols']]
        members = [symbol for symbol in symbols if symbol.kind == Symbol.MEMBER]
        methods = [symbol for symbol in symbols if symbol.kind == Symbol.METHOD]

        return cls(members, methods, LexicalIdentifier(data['name']), data['index'])

    @classmethod
    def from_thing(cls, thing, index):
        members = [elem.symbol().update_index(index) for index, elem in enumerate(thing.members)]
        methods = [elem.symbol().update_index(index) for index, elem in enumerate(thing.methods)]

        return cls(members, methods, thing.name, index)

    def __getitem__(self, item: LexicalIdentifier) -> Symbol:
        return self.lookup[item]

    def __contains__(self, item: LexicalIdentifier) -> bool:
        return item in self.lookup

    def __iter__(self):
        return iter(self.lookup.values())

    def __str__(self):
        return 'SymbolMap({})'.format(self.name)
