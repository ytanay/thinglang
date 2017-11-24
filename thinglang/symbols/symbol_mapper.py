from typing import Tuple, Union, Sequence

from thinglang.compiler.references import ElementReference, LocalReference, Reference
from thinglang.foundation import serializer
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.values.access import Access
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_map import SymbolMap


class SymbolMapper(object):

    """
    The symbol mapper is a container for all the symbol maps needed to perform a compilation pass.
    Its primary function is to resolve compile-time references into the appropriate symbol.
    """

    FOUNDATION = {symbol_map.name: symbol_map for symbol_map in serializer.read_foundation_symbols()}

    def __init__(self, ast=None, include_foundation=True, override=None):
        """
        Creates a new symbol map (generally from a source AST)
        :param ast: the AST being compiled
        :param include_foundation: should foundation classes (base types) be merged into the symbol mapper?
        :param override: add additional symbol maps explicitly
        """
        self.maps = {}

        if include_foundation:
            self.maps.update(SymbolMapper.FOUNDATION)

        if override:
            self.maps.update({symbol_map.name: symbol_map for symbol_map in override})

        if not ast:
            return

        for index, thing in enumerate(ast.children):
            self.maps[thing.name] = SymbolMap.from_thing(thing, index, self.maps.get(thing.extends))

    def resolve(self, target: Union[Identifier, Access], method_locals: dict) -> Reference:
        """
        Resolve a reference into a Reference object
        :param target: the reference being resolved (can be either an identifier or access object)
        :param method_locals: the locals of the method being compiled
        :return: new Reference
        """
        assert not target.STATIC

        if isinstance(target, Identifier):
            return LocalReference(method_locals[target])
        elif isinstance(target, Access):
            return self.resolve_access(target, method_locals)

        raise Exception("Unknown reference type {}".format(target))

    def resolve_partial(self, target: ElementReference, child: Identifier) -> ElementReference:
        """
        Resolve an existing element reference into a a new element reference of one of its children
        :param target: the existing element reference
        :param child: the new field to resolve
        :return: new ElementReference
        """
        return self.resolve_access([target.type, child])

    def resolve_access(self, target: Sequence, method_locals=()) -> ElementReference:
        """
        Resolves an identifier pair (a.b) into an element reference
        :param target: the Access object to resolve
        :param method_locals: the current method's locals
        :return: new ElementReference
        """
        assert len(target) == 2

        first, second, local = target[0], target[1], None
        if first.STATIC:
            container = self.maps[first.type]
        elif first.untyped in self.maps:
            container = self[first]
        elif first in method_locals:
            local = method_locals[first]
            container = self[local.type]
        else:
            raise Exception('Cannot resolve first level access {}'.format(first))

        container, element = self.pull(container, second)

        return ElementReference(container, element, local)

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
                raise Exception('Could not find {} in {} or its parents'.format(item, start))

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
        return self[Identifier('Program')].index

    def __getitem__(self, item) -> SymbolMap:
        """
        If given a GenericIdentifier, generates a new symbol map with the relevant generics filled in.
        Otherwise, returns the symbol map identified by `item`
        """
        if isinstance(item, GenericIdentifier):
            symbol_map = self.maps[item.value]
            parameters = {parameter: replacement for parameter, replacement in zip(symbol_map.generics, item.generics)}
            assert len(symbol_map.generics) == len(parameters)
            return symbol_map.parameterize(parameters)

        return self.maps[item]

    def __contains__(self, item) -> bool:
        """
        Checks if this mapper contains a specific map
        """
        return item in self.maps
