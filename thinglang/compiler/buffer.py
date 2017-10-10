from thinglang.compiler.opcodes import Opcode, OpcodePushLocal, OpcodePushMember
from thinglang.compiler.references import Reference, LocalReference, ElementReference
from thinglang.utils.source_context import SourceReference


class CompilationBuffer(object):
    def __init__(self, symbols, current_locals):
        self.symbols, self.current_locals = symbols, current_locals

        self.instructions = []
        self.data = []
        self.conditional_groups = []

    def append(self, opcode: Opcode, source_ref: SourceReference):
        """
        Append an instruction to this buffer
        """
        if not source_ref:
            raise Exception('Cannot add instruction without a source ref')

        opcode.source_ref = source_ref
        self.instructions.append(opcode)

    def insert(self, index, optional: 'CompilationBuffer'):
        """
        Insert an optional compilation context into this one at a given position
        """

        assert len(optional.instructions) == 1
        assert len(optional.data) == 0
        self.instructions.insert(index, optional.instructions[0])

    def optional(self) -> 'CompilationBuffer':
        """
        Creates an new compilation buffer, which can be optionally merged into the primary buffer
        """
        return CompilationBuffer(self.symbols, self.current_locals)

    def append_static(self, data: bytes) -> int:
        """
        Appends a serialized blob of static data and return its index
        """
        self.data.append(data)
        return len(self.data) - 1

    def epilogue(self, buffer: 'CompilationBuffer'):
        initial = len(self.epilogues)
        self.epilogues.extend(instruction.update_offset(initial, len(self.data)) for instruction in buffer.instructions)
        self.data.extend(buffer.data)
        return initial

    def push_ref(self, ref: Reference, source_ref: SourceReference) -> Reference:
        """
        Push down a reference object into the program stack
        """
        if isinstance(ref, LocalReference):
            self.append(OpcodePushLocal.from_reference(ref), source_ref)
        elif isinstance(ref, ElementReference):
            self.append(OpcodePushMember.from_reference(ref), source_ref)
        else:
            raise Exception('Cannot push down {}'.format(ref))

        return ref

    def resolve(self, item) -> Reference:
        """
        Resolves an arbitrary item into a reference (e.g. LexicalIdentifier, Access)
        """
        return self.symbols.resolve(item, self.current_locals)

    def update_conditional_jumps(self):
        """
        Finalize a conditional jump in the stack of unresolved conditional jumps and pop it off.
        """
        for instruction, jump in list(self.conditional_groups[-1].items())[:-1]:
            jump.update(self.current_index + 1)

        self.conditional_groups.pop()

    @property
    def current_index(self) -> int:
        """
        Returns the index of the current instruction
        """
        return len(self.instructions) - 1

    @property
    def last_instruction(self) -> Opcode:
        """
        Returns the last instruction added to the method-local buffer
        """
        return self.instructions[-1]
