import pprint

from thinglang.compiler.references import Reference
from thinglang.foundation import serializer
from thinglang.parser.nodes.classes import ThingDefinition
from thinglang.parser.nodes.functions import Access
from thinglang.symbols.symbol_map import SymbolMap


class SymbolMapper(object):

    FOUNDATION = {symbol_map.name: symbol_map for symbol_map in serializer.read_foundation_symbols() }

    def __init__(self, ast, include_foundation=True):
        self.maps = {}

        if include_foundation:
            self.maps.update(SymbolMapper.FOUNDATION)

        self.maps.update({
            thing.name: SymbolMap.from_thing(thing, index) for index, thing in enumerate(ast.children)
        })

    def resolve(self, target: Access):
        assert len(target) == 2
        container = self.maps[target[0]]
        element = container[target[1]]
        return Reference(container, element)

    def __getitem__(self, item) -> SymbolMap:
        return self.maps[item]

    def __contains__(self, item) -> bool:
        return item in self.maps

    def index(self, thing: ThingDefinition):
        return self[thing.name].index

    def __str__(self):
        return f'Mapper({pprint.pformat(self.maps)})'


