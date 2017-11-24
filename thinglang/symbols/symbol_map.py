from typing import List

from thinglang.foundation import templates
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.symbol import Symbol


class SymbolMap(object):
    """
    Describes a symbol map - the public fields (members and methods) of a ThingDefinition.
    Each SymbolMap also has an index number, by which it is known to the runtime.
    """

    def __init__(self, members: List[Symbol], methods: List[Symbol], name: Identifier, extends: Identifier, generics: List[Identifier], index: int, offset: int):
        self.members, self.methods, self.name, self.extends, self.generics, self.index, self.offset = \
            members, methods, name, extends, generics or [], index, offset

        self.lookup = {
            elem.name: elem for elem in (self.methods + self.members)
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
            "symbols": [x.serialize() for x in self.lookup.values()]
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

        return cls(members, methods, Identifier(data['name']), Identifier(data['extends']), [Identifier(x) for x in data['generics']], data['index'], data['offset'])

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

    def create_header(self) -> str:
        """
        Creates a C++ header file from this symbol map
        """
        type_cls_name, instance_cls_name = templates.class_names(self.name)

        return templates.FOUNDATION_TYPE_DECLARATION.format(
            type_cls_name=type_cls_name, instance_cls_name=instance_cls_name,
            constructors=templates.format_value_constructor(
                instance_cls_name=instance_cls_name,
                member_list=self.members) if self.members else '',
            mixins=templates.FOUNDATION_MIXINS_DECLARATION if self.members else '',
            members=self.format_member_list('\n', ';'),
            methods=self.format_method_declarations(),
            method_list=self.format_method_list(),
            children=templates.FOUNDATION_CHILDREN if 'list' in self.name.value else ''
        )

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

    def format_member_list(self, separator=', ', delimeter='') -> str:
        """
        Returns a string describing the members of this symbol map
        """
        return separator.join('{} {}{}'.format(x.type.transpile(), x.name.transpile(), delimeter) for x in self.members)

    def format_method_list(self) -> str:
        """
        Returns a string describing the methods of this symbol map
        :return:
        """
        return ', '.join(['&{}'.format(x.name.transpile()) for x in self.methods])

    def format_method_declarations(self) -> str:
        """
        Returns a string with a C++ static void method
        :return:
        """
        return '\n'.join('\tstatic void {}();'.format(x.name.transpile()) for x in self.methods)

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


