import pprint

from thinglang.parser.nodes.classes import ThingDefinition
from thinglang.symbols.symbol_map import SymbolMap


class Mapper(object):

    def __init__(self, ast):
        self.maps = {
            thing.name: SymbolMap(thing, index) for index, thing in enumerate(ast.children)
        }

    def __getitem__(self, item) -> SymbolMap:
        return self.maps[item]

    def __contains__(self, item) -> bool:
        return item in self.maps

    def index(self, thing: ThingDefinition):
        return self[thing.name].index

    def __str__(self):
        return f'Mapper({pprint.pformat(self.maps)})'
