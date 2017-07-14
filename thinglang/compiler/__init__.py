import struct

from thinglang.compiler.opcodes import OpcodePushStatic, Opcode, OpcodeMethodEnd, OpcodePush, OpcodeMethodDefinition
from thinglang.compiler.references import ResolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier


class CompilationContext(object):

    def __init__(self):
        self.symbols = []
        self.data = []
        self.current_method = []
        self.conditional_groups = []

    def append(self, symbol):
        if isinstance(symbol, Opcode):
            self.current_method.append(symbol)
        elif symbol:
            self.current_method.extend(symbol)

        return symbol, self.current_index()

    def finalize(self):
        data = bytes().join(x for x in self.data)
        code = bytes().join(x.resolve() for x in self.symbols + self.current_method)
        header = bytes('THING', 'utf-8') + struct.pack('<HII', 1, len(data) + len(code), len(data))

        return header + data + code

    def append_static(self, data):
        self.data.append(data)
        return len(self.data) - 1

    def current_index(self):
        return len(self.current_method) - 1

    def push_down(self, value):
        idx = self.current_index()
        if isinstance(value, ResolvedReference) or value.implements(LexicalIdentifier):
            assert value.index is not None, 'Unresolved reference {}'.format(value)
            self.append(OpcodePush(value.index))
        elif value.STATIC:
            self.append(OpcodePushStatic(self.append_static(value.serialize())))
        else:
            value.compile(self)
        return idx

    def method_start(self, *args):
        self.symbols += self.current_method
        self.current_method = [
            OpcodeMethodDefinition(*args)
        ]

    def method_end(self):
        self.current_method.append(OpcodeMethodEnd())

    def last(self):
        return self.current_method[-1], len(self.current_method) - 1

    def update_conditional_jumps(self):
        for symbol, jump in list(self.conditional_groups[-1].items())[:-1]:
            jump.update(self.current_index())

        self.conditional_groups.pop()
