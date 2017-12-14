import collections
from typing import List

from thinglang.foundation import templates
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.merged_symbol import MergedSymbol
from thinglang.symbols.symbol import Symbol
from thinglang.utils import collection_utils


class SymbolMap(object):
    """
    Describes a symbol map - the public fields (members and methods) of a ThingDefinition.
    Each SymbolMap also has an index number, by which it is known to the runtime.
    """

    def __init__(self, members: List[Symbol], methods: List[Symbol], name: Identifier, extends: Identifier, generics: List[Identifier], index: int, offset: int):
        self.members, self.methods, self.name, self.extends, self.generics, self.index, self.offset = \
            members, self.merge_method_symbols(methods), name, extends, generics or [], index, offset

        self.lookup = {
            symbol.name: symbol for symbol in self.members + self.methods
        }

        assert len(self.methods) + len(self.members) == len(self.lookup), 'Thing definition contains colliding elements'

    def override_index(self, new_index):
        """
        Sets a new index for this SymbolMap
        """
        self.index = new_index

    def serialize(self) -> dict:
        """
        Serialize this symbol map (and its symbols) into a dict
        """
        return {
            "name": self.name,
            "extends": self.extends,
            "generics": self.generics,
            "index": self.index,
            "offset": self.offset,
            "symbols": collection_utils.flatten([x.serialize() for x in self.lookup.values()])
        }

    @classmethod
    def from_serialized(cls, data: dict) -> 'SymbolMap':
        """
        Reads a serialized symbol map and returns a new SymbolMap object.
        Additionally, deserializes its symbols into Symbol objects
        """
        symbols = [Symbol.load(elem) for elem in data['symbols']]
        members = [symbol for symbol in symbols if symbol.kind == Symbol.MEMBER]
        methods = [symbol for symbol in symbols if symbol.kind == Symbol.METHOD]
        extends = Identifier(data['extends']) if data['extends'] else None

        return cls(members, methods, Identifier(data['name']), extends, [Identifier(x) for x in data['generics']], data['index'], data['offset'])

    @classmethod
    def from_thing(cls, thing, index: int, extends: 'SymbolMap') -> 'SymbolMap':
        """
        Creates a new Symbol map from a ThingDefinition
        :param thing: the source ThingDefinition
        :param index: the index of the new symbol map
        :param extends: optionally, the symbol map from which this thing inherits
        """
        offset = extends.offset if extends is not None else 0

        members = [elem.symbol().update_index(offset + index) for index, elem in enumerate(thing.members)]
        methods = [elem.symbol().update_index(index) for index, elem in enumerate(thing.methods)]

        return cls(members, methods, thing.name, thing.extends, thing.generics, index, len(members) + offset)

    def parameterize(self, parameters: dict) -> 'SymbolMap':
        """
        Creates a new SymbolMap, replacing the generic parameters in this SymbolMap with determined values
        :param parameters: a mapping of generic name -> resolved name
        """
        assert set(parameters.keys()) == set(self.generics), 'Partial parameterization is not allowed'

        return SymbolMap(
            [x.parameterize(parameters) for x in self.members],
            [x.parameterize(parameters) for x in self.methods],
            Identifier('{}:<{}>'.format(self.name, parameters)),
            self.extends,
            [],
            self.index,
            self.offset
        )

    def __getitem__(self, item: Identifier) -> Symbol:
        """
        Returns a symbol from this map
        """
        return self.lookup[item]

    def __contains__(self, item: Identifier) -> bool:
        """
        Checks if a symbol identified by `item` exists
        """
        return item in self.lookup

    def __iter__(self):
        """
        Iterates over all the fields of this symbol map
        """
        return iter(self.lookup.values())

    def __repr__(self):
        return f'SymbolMap({self.name})'

    @staticmethod
    @collection_utils.drain()
    def merge_method_symbols(methods):
        method_symbols = collections.defaultdict(list)

        for method_symbol in methods:
            method_symbols[method_symbol.name].append(method_symbol)

        for symbol_name, symbols in method_symbols.items():
            yield symbols[0] if len(symbols) == 1 else MergedSymbol(symbols)
