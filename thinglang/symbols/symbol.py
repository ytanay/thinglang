from thinglang.lexer.values.identifier import Identifier


class Symbol(object):

    METHOD, MEMBER = object(), object()
    INTERNAL, BYTECODE = object(), object()
    PUBLIC = object()

    def __init__(self, name, kind, type, static, arguments=None, index=None, convention=BYTECODE):
        super(Symbol, self).__init__()

        self.name, self.kind, self.type, self.static, self.arguments, self.index, self._convention = \
            name, kind, type, static, arguments, index, convention
        self.visibility = Symbol.PUBLIC

    def update_index(self, new_index):
        self.index = new_index
        return self

    @property
    def convention(self):
        return self._convention

    @convention.setter
    def convention(self, value):
        self._convention = value

    def serialize(self):
        return {
            "name": self.name,
            "index": self.index,
            "kind": "method" if self.kind is Symbol.METHOD else "member",
            "type": self.type,
            "static": self.static,
            "arguments": self.arguments,
            "convention": "bytecode" if self.convention is Symbol.BYTECODE else "internal"
        }

    @classmethod
    def load(cls, data: dict) -> 'Symbol':
        assert data['kind'] in ('member', 'method')
        assert data['convention'] in ('user', 'internal')

        return cls(
            name=Identifier(data['name']),
            kind=Symbol.METHOD if data['kind'] == 'method' else Symbol.MEMBER,
            type=Identifier(data['type']),
            static=data['static'],
            arguments=data['arguments'] is not None and [Identifier(x) for x in data['arguments']],
            index=data['index'],
            convention=Symbol.BYTECODE if data['convention'] == 'bytecode' else Symbol.INTERNAL
        )

    @classmethod
    def method(cls, name, return_type, static, arguments):
        return cls(name, cls.METHOD, return_type, static, [x.type for x in arguments])

    @classmethod
    def member(cls, name, type):
        return cls(name, cls.MEMBER, type, False)
