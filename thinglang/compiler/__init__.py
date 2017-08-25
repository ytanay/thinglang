import struct

from thinglang.compiler.opcodes import OpcodePushStatic, Opcode, OpcodeMethodEnd, OpcodePushLocal, \
    OpcodeMethodDefinition, OpcodePushMember, OpcodePopLocal, OpcodePopMember
from thinglang.compiler.references import ElementReference, LocalReference, StaticReference, Reference
from thinglang.lexer.tokens.base import LexicalIdentifier


class CompilationContext(object):

    def __init__(self, symbols, entry=None):
        self.symbols = symbols

        self.current_locals = None
        self.entry = entry or 0

        self.instructions = []
        self.data = []
        self.instruction_block = []
        self.conditional_groups = []

    def append(self, symbol):
        self.instruction_block.append(symbol)
        return symbol, self.current_index()

    def bytes(self):
        data = bytes().join(x for x in self.data)
        code = bytes().join(x.resolve() for x in self.instructions + self.instruction_block)
        header = bytes('THING\x0C', 'utf-8') + struct.pack('<HIII', 1, len(data) + len(code), len(data), self.entry)

        return header + data + code

    def append_static(self, data):
        self.data.append(data)
        return len(self.data) - 1

    def current_index(self):
        return len(self.instruction_block) - 1

    def push_ref(self, ref):
        """
        Push down an arbitrary reference
        """

        if isinstance(ref, StaticReference):
            self.append(OpcodePushStatic(self.append_static(ref.value.serialize())))
        elif isinstance(ref, LocalReference):
            self.append(OpcodePushLocal.from_reference(ref))
        elif isinstance(ref, ElementReference):
            self.append(OpcodePushMember.from_reference(ref))
        else:
            raise Exception('Cannot push down {}'.format(ref))

    def method_start(self, method_locals, *args):
        self.instructions += self.instruction_block
        self.current_locals = method_locals

        self.instruction_block = [
            OpcodeMethodDefinition(*args)
        ]

    def method_end(self):
        self.instruction_block.append(OpcodeMethodEnd())

    def update_conditional_jumps(self):
        for symbol, jump in list(self.conditional_groups[-1].items())[:-1]:
            jump.update(self.current_index())

        self.conditional_groups.pop()

    def resolve(self, ref):
        return self.symbols.resolve(ref, self.current_locals)
