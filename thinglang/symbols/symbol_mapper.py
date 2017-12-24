from typing import Tuple, Union, Sequence

import itertools

from thinglang.compiler.errors import InvalidReference
from thinglang.compiler.references import ElementReference, LocalReference, Reference
from thinglang.foundation import serializer
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.values.indexed_access import IndexedAccess
from thinglang.parser.values.named_access import NamedAccess
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_map import SymbolMap


class SymbolMapper(object):

    """
    The symbol mapper is a container for all the symbol maps needed to perform a compilation pass.
    Its primary function is to resolve compile-time references into the appropriate symbol.
    """

    FOUNDATION = {symbol_map.name: symbol_map for symbol_map in serializer.read_foundation_symbols()}
    INDEX_GETTER_NAME = Identifier('get')

    def __init__(self, ast=None, include_foundation=True):
        """
        Creates a new symbol map (generally from a source AST)
        :param ast: the AST being compiled
        :param include_foundation: should foundation classes (base types) be merged into the symbol mapper?
        """
        self.maps = {}
        self.indexer = itertools.count()
        self.internal_indexing = {}
        self.user_indexing = {}

        if include_foundation:
            self.maps.update(SymbolMapper.FOUNDATION)

        if ast:
            for index, thing in enumerate(x for x in ast.children if isinstance(x, ThingDefinition)):
                self.maps[thing.name] = SymbolMap.from_thing(thing, self.maps.get(thing.extends))
                self.user_indexing[thing.name] = index

    def resolve(self, target: Union[Identifier, NamedAccess], method_locals: dict) -> Reference:
        """
        Resolve a reference into a Reference object
        :param target: the reference being resolved (can be either an identifier or access object)
        :param method_locals: the locals of the method being compiled
        :return: new Reference
        """
        assert not target.STATIC

        if isinstance(target, Identifier):
            return LocalReference(method_locals[target], target)
        elif isinstance(target, NamedAccess):
            return self.resolve_named(target, method_locals)

        raise Exception("Unknown reference type {}".format(target))

    def resolve_partial(self, target: ElementReference, child: Identifier) -> ElementReference:
        """
        Resolve an existing element reference into a a new element reference of one of its children
        :param target: the existing element reference
        :param child: the new field to resolve
        :return: new ElementReference
        """
        return self.resolve_named([target.type, child])

    def resolve_named(self, target: Sequence, method_locals=()) -> ElementReference:
        """
        Resolves an identifier pair (a.b) into an element reference
        :param target: the Access object to resolve
        :param method_locals: the current method's locals
        :return: new ElementReference
        """
        assert len(target) == 2

        first, second, local = target[0], target[1], None

        if first.STATIC:
            container = self[first.type]
        elif isinstance(first, IndexedAccess):
            container = self.resolve_indexed(first, method_locals)
        elif first.untyped in self.maps:
            container = self[first]
        elif first in method_locals:
            local = method_locals[first]
            container = self[local.type]
        else:
            raise Exception('Cannot resolve first level access {} (on {}) from {}'.format(first, first.source_ref, method_locals))

        container, element = self.pull(container, second)

        return ElementReference(self.index(container), element, local)

    def resolve_indexed(self, access: IndexedAccess, method_locals=()) -> SymbolMap:
        """
        Resolves an IndexedAccess object into a symbol map describing the type of the indexed property.
        Assumes the getter method is called "get"
        """
        target, index = access.target, access.index
        resolved = self.resolve(target, method_locals)
        getter = self[resolved.type][self.INDEX_GETTER_NAME]
        return self[getter.type]

    def pull(self, start: SymbolMap, item: Identifier) -> Tuple[SymbolMap, Symbol]:
        """
        Pull a symbol from a symbol map, iteratively traversing its parents until a match is found
        :param start: the original symbol map
        :param item: the item to find
        :return: a pair of SymbolMap, Symbol
        """
        container = start

        while item not in container:
            if container.extends:
                container = self[container.extends]
            else:
                raise InvalidReference(item, start)

        return container, container[item]

    def inheritance(self, start):
        """
        Emits an inheritance chain (from descendant to ancestor)
        :param start: the ThingDefinition to start from
        """
        current = self[start.name]
        yield current

        while current.extends:
            current = self[current.extends]
            yield current

    def entry(self) -> int:
        """
        Get the index of the program's entry point
        """
        return self.user_indexing[Identifier('Program')]

    @property
    def indexed(self):
        """
        Returns a sorted list of the indexed symbol maps in this mapper
        """
        return sorted(((name, index) for name, index in self.internal_indexing.items() if self.maps[name].convention is Symbol.INTERNAL),
                      key=lambda x: x[1])

    def index(self, symbol_map):
        if symbol_map.convention == Symbol.INTERNAL:
            return self.internal_indexing[symbol_map.name.untyped]
        else:
            return self.user_indexing[symbol_map.name.untyped]

    def __getitem__(self, item) -> SymbolMap:
        """
        If given a GenericIdentifier, generates a new symbol map with the relevant generics filled in.
        Otherwise, returns the symbol map identified by `item`
        """
        if isinstance(item, GenericIdentifier):
            symbol_map = self[item.value]
            parameters = {parameter: replacement for parameter, replacement in zip(symbol_map.generics, item.generics)}
            assert len(symbol_map.generics) == len(parameters)
            return symbol_map.parameterize(parameters)

        symbol_map = self.maps[item]

        if item not in self.user_indexing and item not in self.internal_indexing:
            self.internal_indexing[item] = next(self.indexer)

        return symbol_map

    def __contains__(self, item) -> bool:
        """
        Checks if this mapper contains a specific map
        """
        return item in self.maps
