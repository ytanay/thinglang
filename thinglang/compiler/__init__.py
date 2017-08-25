import struct

from thinglang.compiler.opcodes import OpcodePushStatic, Opcode, OpcodeMethodEnd, OpcodePushLocal, \
    OpcodeMethodDefinition, OpcodePushMember, OpcodePopLocal, OpcodePopMember
from thinglang.compiler.references import ElementReference, LocalReference, StaticReference, Reference


class CompilationContext(object):

    def __init__(self, symbols, entry=None):

        self.symbols = symbols

        self.current_locals = None
        self.entry = entry or 0

        self.instructions = []
        self.data = []
        self.instruction_block = []
        self.conditional_groups = []

    def append(self, opcode: Opcode) -> None:
        """
        Append an opcode to the instruction block of the current method
        """

        self.instruction_block.append(opcode)

    def append_static(self, data: bytes) -> int:
        """
        Add a serialized blob of static data and return its index
        """

        self.data.append(data)
        return len(self.data) - 1

    def current_index(self) -> int:
        """
        Returns the index of the current instruction
        """

        return len(self.instruction_block) - 1

    def resolve(self, item) -> Reference:
        """
        Resolves an arbitrary item into a reference (e.g. LexicalIdentifier, Access)
        """

        return self.symbols.resolve(item, self.current_locals)

    def push_ref(self, ref: Reference) -> Reference:
        """
        Push down a reference object into the program stack
        """

        if isinstance(ref, StaticReference):
            self.append(OpcodePushStatic(self.append_static(ref.value.serialize())))
        elif isinstance(ref, LocalReference):
            self.append(OpcodePushLocal.from_reference(ref))
        elif isinstance(ref, ElementReference):
            self.append(OpcodePushMember.from_reference(ref))
        else:
            raise Exception('Cannot push down {}'.format(ref))

        return ref

    def method_start(self, method_locals, *args) -> None:
        """
        Mark the start of the method using a method definition Opcode.
        Additionally, updates the list of available locals, and flushes the instruction block.
        """

        self.instructions += self.instruction_block
        self.current_locals = method_locals

        self.instruction_block = [
            OpcodeMethodDefinition(*args)
        ]

    def method_end(self) -> None:
        """
        Mark the end of a method
        """

        self.instruction_block.append(OpcodeMethodEnd())

    def update_conditional_jumps(self) -> None:
        """
        Finalize a conditional jump in the stack of unresolved conditional jumps and pop it off.
        """

        for symbol, jump in list(self.conditional_groups[-1].items())[:-1]:
            jump.update(self.current_index())

        self.conditional_groups.pop()

    def bytes(self) -> bytes:
        """
        Serializes the compilation context into thinglang bytecode
        """

        data = bytes().join(x for x in self.data)
        code = bytes().join(x.resolve() for x in self.instructions + self.instruction_block)
        header = bytes('THING\x0C', 'utf-8') + struct.pack('<HIII', 1, len(data) + len(code), len(data), self.entry)

        return header + data + code
