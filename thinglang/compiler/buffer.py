from thinglang.compiler.errors import CalledInstanceMethodOnClass
from thinglang.compiler.opcodes import Opcode, OpcodePushLocal, OpcodePushMember
from thinglang.compiler.references import Reference, LocalReference, ElementReference
from thinglang.compiler.tracker import LocalTracker
from thinglang.utils.source_context import SourceReference


class CompilationBuffer(object):
    """
    These buffers hold generated bytecode and static data collected during compilation.
    In certain cases, a buffer can be merged into another buffer, updating relevant offsets in the process
    """

    USED_ALIAS = object()

    def __init__(self, symbols, current_locals, current_generics, track=True, require_source_refs=True):
        self.symbols, self.current_locals, self.current_generics, self.track, self.require_source_refs = symbols, current_locals, current_generics or (), track, require_source_refs

        self.instructions = []
        self.epilogues = []
        self.data = []
        self.conditional_groups = []
        self.exception_table = []

    def append(self, opcode: Opcode, source_ref: SourceReference):
        """
        Append an instruction to this buffer
        """
        if not source_ref and self.require_source_refs:
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

    def extend(self, buffer: 'CompilationBuffer'):
        self.instructions.extend(instruction.update_offset(len(self.instructions), len(self.data)) for instruction in buffer.instructions)
        self.data.extend(buffer.data)

    def optional(self, arguments=None, track=False, require_source_refs=None) -> 'CompilationBuffer':
        """
        Creates an new compilation buffer, which can be optionally merged into the primary buffer
        """
        current_locals = self.current_locals if arguments is None else {x: LocalTracker(x.type) for x in arguments}
        return CompilationBuffer(self.symbols, current_locals, self.current_generics, track, self.require_source_refs if require_source_refs is None else require_source_refs)

    def append_static(self, data: bytes) -> int:
        """
        Appends a serialized blob of static data and return its index
        """
        self.data.append(data)
        return len(self.data) - 1

    def add_entries(self, entries):
        """
        Add a list of entries to the exception handling table.
        """
        self.exception_table.extend(reversed(entries))

    def epilogue(self, buffer: 'CompilationBuffer'):
        initial = len(self.epilogues)
        self.epilogues.extend(instruction.update_offset(initial, len(self.data), True) for instruction in buffer.instructions)
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
        elif isinstance(ref, Reference):
            raise CalledInstanceMethodOnClass(ref, source_ref)
        else:
            raise Exception('Cannot push down {}'.format(ref))

        return ref

    def resolve(self, item) -> Reference:
        """
        Resolves an arbitrary item into a reference (e.g. LexicalIdentifier, Access)
        """
        resolved = self.symbols.resolve(item, self.current_locals, self.current_generics)

        if self.track:
            resolved.hit()

        return resolved

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
    def next_index(self) -> int:
        """
        Returns the index of the next instruction
        """
        return len(self.instructions)

    @property
    def last_instruction(self) -> Opcode:
        """
        Returns the last instruction added to the method-local buffer
        """
        return self.instructions[-1]

