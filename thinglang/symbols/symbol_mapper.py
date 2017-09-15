from thinglang.compiler.references import ElementReference, LocalReference, StaticReference, Reference
from thinglang.foundation import serializer
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.definitions.thing_definition import ThingDefinition
from thinglang.parser.nodes.values.access import Access
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_map import SymbolMap


class SymbolMapper(object):

    FOUNDATION = {symbol_map.name: symbol_map for symbol_map in serializer.read_foundation_symbols()}

    def __init__(self, ast=None, include_foundation=True, override=None):
        self.maps = {}

        if include_foundation:
            self.maps.update(SymbolMapper.FOUNDATION)

        if override:
            self.maps.update({symbol_map.name: symbol_map for symbol_map in override})

        if ast:
            self.maps.update({
                thing.name: SymbolMap.from_thing(thing, index) for index, thing in enumerate(ast.children)
            })

    def resolve(self, target, locals, next_item=None):

        if next_item is not None:
            assert isinstance(target, Reference)
            return self.resolve_access([target.type, next_item])

        if target.implements(LexicalIdentifier):
            return LocalReference(locals[target])
        elif target.STATIC:
            return StaticReference(target)
        elif target.implements(Access):
            return self.resolve_access(target, locals)

        raise Exception("Unknown reference type {}".format(target))

    def resolve_access(self, target, locals=()):
        assert len(target) == 2

        first, second, local = target[0], target[1], None
        if first.STATIC:
            container = self.maps[first.type]
        elif first in self.maps:
            container = self.maps[first]
        elif first in locals:
            local = locals[first]
            container = self.maps[local.type]
        else:
            raise Exception('Cannot resolve first level access {}'.format(first))

        element = container[second]

        return ElementReference(container, element, local)

    def index(self, thing: ThingDefinition):
        return self[thing.name].index

    def entry(self):
        return self[LexicalIdentifier('Program')].index

    def dereference(self, parent: Symbol, child: LexicalIdentifier):
        symbol = self.maps[parent.type][child]
        return ElementReference(self.maps[symbol.type], symbol)

    def __getitem__(self, item) -> SymbolMap:
        return self.maps[item]

    def __contains__(self, item) -> bool:
        return item in self.maps
