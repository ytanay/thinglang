from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.phases import preprocess
from thinglang.symbols.argument_selector import ArgumentSelector
from thinglang.symbols.inline_candidate import InlineCandidate
from thinglang.utils.source_context import SourceContext


class Symbol(object):
    """
    Describes a public (i.e. exported) symbol, which can be either a member or a method
    Symbols are strictly ordered, and their indices in this ordering is how the runtime refers to symbols.
    """

    METHOD, MEMBER = object(), object()
    INTERNAL, BYTECODE = object(), object()  # The calling convention used, if this symbol is a method
    PUBLIC, PRIVATE = object(), object()  # The visibility of this symbol

    def __init__(self, name: Identifier, kind, type: Identifier, static: bool, visibility=PUBLIC, arguments=None, index=None, convention=BYTECODE, node=None):
        super(Symbol, self).__init__()

        self.name, self.kind, self.type, self.static, self.visibility, self.arguments, self.index, self._convention, self.node = \
            name, kind, type, static, visibility, arguments, index, convention, node

    def update_index(self, new_index: int):
        """
        Override the index of this symbol
        """
        self.index = new_index
        return self

    def parameterize(self, parameters: dict) -> 'Symbol':
        """
        Creates a new symbol, with generic parameters replaced by their determined values
        :param parameters: a mapping of generic name -> resolved name
        """
        return Symbol(self.name,
                      self.kind,
                      self.type.parameterize(parameters) if self.type else None,
                      self.static,
                      self.visibility,
                      [x.parameterize(parameters) for x in self.arguments] if self.arguments else self.arguments,
                      self.index,
                      self.convention)

    def selector(self):
        return ArgumentSelector([self])

    @property
    def convention(self):
        """
        Returns the calling convention for this symbol
        """
        return self._convention

    @convention.setter
    def convention(self, value):
        """
        Update the calling convention for this symbol
        """
        assert value in (Symbol.INTERNAL, Symbol.BYTECODE)
        self._convention = value

    def serialize(self) -> dict:
        """
        Returns a dict representing this symbol
        """
        return {
            "name": self.name,
            "index": self.index,
            "kind": "method" if self.kind is Symbol.METHOD else "member",
            "type": self.type,
            "static": self.static,
            "arguments": self.arguments,
            "visibility": "public" if self.visibility is Symbol.PUBLIC else "private",
            "convention": self.serialize_convention(self.convention),
            "inline": self.node.serialize() if self.node else None
        }

    @classmethod
    def load(cls, data: dict) -> 'Symbol':
        """
        Loads a serialized symbol
        """
        assert data['kind'] in ('member', 'method')
        assert data['convention'] in ('bytecode', 'internal')

        arguments = data['arguments'] is not None and [cls.load_identifier(x) for x in data['arguments']]

        return cls(
            name=cls.serialize_name(data['name']),
            kind=Symbol.METHOD if data['kind'] == 'method' else Symbol.MEMBER,
            type=cls.load_identifier(data['type']),
            static=data['static'],
            visibility=Symbol.PUBLIC if data['visibility'] == 'public' else Symbol.PRIVATE,
            arguments=arguments,
            index=data['index'],
            convention=cls.serialize_convention(data['convention']),
            node=InlineCandidate.from_serialized(data['inline']['code'], data['inline']['argument_names'], arguments) if data['inline'] else None
        )

    @staticmethod
    def load_identifier(value) -> Identifier:
        """
        Parse a generic identifier
        """
        if isinstance(value, str):
            return Identifier(value)
        elif isinstance(value, list):
            return GenericIdentifier(Identifier(value[0]), tuple(Identifier(x) for x in value[1]))

    @classmethod
    def method(cls, name: Identifier, return_type: Identifier, static: bool, arguments: list, node) -> 'Symbol':
        """
        Helper method to create a new method symbol
        """
        return cls(name, cls.METHOD, return_type, static, Symbol.PUBLIC, [x.type for x in arguments], node=node)

    @classmethod
    def member(cls, name: Identifier, type: Identifier, visibility) -> 'Symbol':
        """
        Helper method to create a new member symbol
        """
        return cls(name, cls.MEMBER, type, False, visibility)

    def __repr__(self):
        return f'Symbol({self.name})'

    @classmethod
    def serialize_convention(cls, param):
        if isinstance(param, str):
            return Symbol.BYTECODE if param == 'bytecode' else Symbol.INTERNAL
        else:
            return "bytecode" if param is Symbol.BYTECODE else "internal"

    @classmethod
    def serialize_name(cls, param):
        if isinstance(param, str):
            return CastTag.parse(param) if CastTag.matches(param) else Identifier(param)
        else:
            return repr(param)
