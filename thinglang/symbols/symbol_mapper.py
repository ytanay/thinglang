from typing import Tuple, Union, Sequence

from thinglang.compiler.references import ElementReference, LocalReference, Reference
from thinglang.foundation import serializer
from thinglang.lexer.values.identifier import Identifier
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

        if ast:
            self.maps.update({
                thing.name: SymbolMap.from_thing(thing, index) for index, thing in enumerate(ast.children)
            })

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
        elif first in self.maps:
            container = self.maps[first]
        elif first in method_locals:
            local = method_locals[first]
            container = self.maps[local.type]
        else:
            raise Exception('Cannot resolve first level access {}'.format(first))

        container, element = self.pull(container, second)

        return ElementReference(container, element, local)

    def pull(self, container: SymbolMap, item: Identifier) -> Tuple[SymbolMap, Symbol]:
        """
        Pull a symbol from a symbol map, iteratively traversing its parents until a match is found
        :param container: the original symbol map
        :param item: the item to find
        :return: a pair of SymbolMap, Symbol
        """
        while item not in container:
            if container.extends:
                container = self.maps[container.extends]
            else:
                raise Exception('Could not find {} in {} or its parents'.format(item, container))

        return container, container[item]

    def entry(self) -> int:
        """
        Get the index of the program's entry point
        """
        return self[Identifier('Program')].index

    def __getitem__(self, item) -> SymbolMap:
        return self.maps[item]

    def __contains__(self, item) -> bool:
        return item in self.maps
