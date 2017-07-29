import pprint

from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.classes import ThingDefinition
from thinglang.symbols.symbol import Symbol


class SymbolMap(object):

    def __init__(self, thing: ThingDefinition, index: int):
        self.thing = thing
        self.index = index

        self.methods = [elem.symbol().update_index(index) for index, elem in enumerate(thing.methods())]
        self.members = [elem.symbol().update_index(index) for index, elem in enumerate(thing.members())]

        self.lookup = {
            elem.name: elem for elem in (self.methods + self.members)
        }

        assert len(self.methods) + len(self.members) == len(self.lookup), 'Thing definition contains colliding elements'

    def __getitem__(self, item: LexicalIdentifier) -> Symbol:
        return self.lookup[item]

    def __contains__(self, item: LexicalIdentifier) -> bool:
        return item in self.lookup

    def serialize(self):
        return [x.serialize() for x in self.lookup.values()]

    def __repr__(self) -> str:
        return 'SymbolMap({{{}}})'.format(pprint.pformat(self.lookup))