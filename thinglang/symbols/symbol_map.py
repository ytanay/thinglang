import collections
import struct
from typing import List

from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.symbols.merged_symbol import MergedSymbol
from thinglang.symbols.symbol import Symbol
from thinglang.utils import collection_utils


class SymbolMap(object):
    """
    Describes a symbol map - the public fields (members and methods) of a ThingDefinition.
    Each SymbolMap also has an index number, by which it is known to the runtime.
    """

    def __init__(self, members: List[Symbol], methods: List[Symbol], name: Identifier, extends: Identifier, generics: List[Identifier], convention, member_offset: int=0, method_offset: int=0):
        self.members, self.methods, self.name, self.extends, self.generics, self.convention, self.member_offset, self.method_offset = \
            members, self.merge_method_symbols(methods), name, extends, generics or [], convention, member_offset, method_offset

        self.lookup = {
            symbol.name: symbol for symbol in self.members + self.methods
        }

        assert len(self.methods) + len(self.members) == len(self.lookup), 'Thing definition contains colliding elements'
        assert {x.convention for x in self.lookup.values()} == {self.convention}, 'Inconsistent calling conventions identified'

    def serialize(self) -> dict:
        """
        Serialize this symbol map (and its symbols) into a dict
        """
        return {
            "name": self.name,
            "extends": self.extends,
            "generics": self.generics,
            "offsets": {
                "members": self.member_offset,
                "methods": self.method_offset
            },
            "convention": Symbol.serialize_convention(self.convention),
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

        return cls(members=members,
                   methods=methods,
                   name=Identifier(data['name']),
                   extends=extends,
                   generics=[Identifier(x) for x in data['generics']],
                   convention=Symbol.serialize_convention(data['convention']),
                   member_offset=data['offsets']['members'],
                   method_offset=data['offsets']['methods'])

    @classmethod
    def from_thing(cls, thing, extends: 'SymbolMap') -> 'SymbolMap':
        """
        Creates a new Symbol map from a ThingDefinition
        :param thing: the source ThingDefinition
        :param index: the index of the new symbol map
        :param extends: optionally, the symbol map from which this thing inherits
        """

        member_offset, method_offset = 0, 0

        if extends is not None:
            member_offset, method_offset = len(extends.members) + extends.member_offset, len(extends.methods) + extends.method_offset

        members = [elem.symbol().update_index(member_offset + index) for index, elem in enumerate(thing.members)]
        methods = [elem.symbol().update_index(method_offset + index) for index, elem in enumerate(thing.methods)]

        return cls(members,
                   methods,
                   thing.name,
                   thing.extends,
                   thing.generics,
                   Symbol.BYTECODE,
                   member_offset=member_offset,
                   method_offset=method_offset)

    def parameterize(self, parameters: dict) -> 'SymbolMap':
        """
        Creates a new SymbolMap, replacing the generic parameters in this SymbolMap with determined values
        :param parameters: a mapping of generic name -> resolved name
        """
        assert set(parameters.keys()) == set(self.generics), 'Partial parameterization is not allowed'

        return SymbolMap(
            [x.parameterize(parameters) for x in self.members],
            [x.parameterize(parameters) for x in self.methods],
            GenericIdentifier(self.name, tuple([parameters[x] for x in self.generics])),
            self.extends,
            [],
            self.convention,
            self.member_offset,
            self.method_offset)

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
            yield symbols.pop() if len(symbols) == 1 else MergedSymbol(symbols)
