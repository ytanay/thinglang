import struct

from thinglang.compiler.opcodes import OPCODES
from thinglang.compiler.references import ResolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier


class ResolvableInstruction(object):

    def __init__(self, format, opcode, *args):
        self.format, self.opcode, self.args = format, opcode, args

    def resolve(self):
        return struct.pack(self.format, self.opcode, *self.args)


class BytecodeSymbols(object):

    @classmethod
    def push(cls, id):
        return struct.pack('<BI', OPCODES['PUSH'], id)

    @classmethod
    def push_static(cls, id):
        return struct.pack('<BI', OPCODES['PUSH_STATIC'], id)

    @classmethod
    def set_static(cls, idx, val):
        return struct.pack('<BII', OPCODES['SET_STATIC'], idx if isinstance(idx, int) else idx[0], val)

    @classmethod
    def set(cls, idx):
        return struct.pack('<BI', OPCODES['SET'], idx if isinstance(idx, int) else idx[0])

    @classmethod
    def call(cls, type_id, idx):
        return struct.pack('<BII', OPCODES['CALL'], type_id, idx)

    @classmethod
    def call_internal(cls, thing, idx):
        return struct.pack('<BII', OPCODES['CALL_INTERNAL'], thing, idx)

    @classmethod
    def method_end(cls):
        return struct.pack('<B', OPCODES['METHOD_END'])

    @classmethod
    def pop(cls):
        return struct.pack('<B', OPCODES['POP'])

    @classmethod
    def push_null(cls):
        return struct.pack('<B', OPCODES['PUSH_NULL'])

    @classmethod
    def returns(cls):
        return struct.pack('<B', OPCODES['RETURN'])

    @classmethod
    def conditional_jump(cls, idx=None):
        return ResolvableInstruction('<BI', OPCODES['CONDITIONAL_JUMP'], idx)

    @classmethod
    def jump(cls, idx=None):
        return ResolvableInstruction('<BI', OPCODES['JUMP'], idx)


class CompilationContext(object):

    def __init__(self):
        self.symbols = []
        self.data = []
        self.current_method = []
        self.conditional_groups = []

    def append(self, symbol):
        if isinstance(symbol, (ResolvableInstruction, bytes)):
            self.current_method.append(symbol)
        elif symbol:
            self.current_method.extend(symbol)
        return symbol, self.current_index()

    def finalize(self):
        code = bytes().join(x.resolve() if isinstance(x, ResolvableInstruction) else x for x in self.symbols + self.current_method)
        data = bytes().join(x for x in self.data)
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
            self.append(BytecodeSymbols.push(value.index))
        elif value.STATIC:
            self.append(BytecodeSymbols.push_static(self.append_static(value.serialize())))
        else:
            value.compile(self)
        return idx

    def method_start(self):
        self.symbols += self.current_method
        self.current_method = []

    def method_end(self):
        self.current_method.append(BytecodeSymbols.method_end())

    def last(self):
        return self.current_method[-1], len(self.current_method) - 1

    def update_conditional_jumps(self):
        print(self.conditional_groups[-1])
        for symbol, jump in list(self.conditional_groups[-1].items())[:-1]:

            jump.args = self.current_index(),


        self.conditional_groups.pop()