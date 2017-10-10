import collections
import struct

from thinglang.compiler.opcodes import Opcode, OpcodePushLocal, \
    OpcodePushMember
from thinglang.compiler.sentinels import SentinelMethodDefinition, SentinelMethodEnd, SentinelCodeEnd, SentinelDataEnd
from thinglang.compiler.references import ElementReference, LocalReference, Reference
from thinglang.utils import collection_utils
from thinglang.utils.source_context import SourceReference, SourceContext

HEADER_FORMAT = '<HIII'
BytecodeHeader = collections.namedtuple('BytecodeHeader', [
    'version',
    'instruction_count',
    'data_item_count',
    'entrypoint'
])


class CompilationContext(object):

    def __init__(self, symbols, source: SourceContext, entry=None):

        self.symbols = symbols
        self.source = source

        self.current_locals = None
        self.entry = entry or 0

        self.instructions = []
        self.data = []
        self.instruction_block = []
        self.epilogues = []
        self.conditional_groups = []

    def append(self, opcode: Opcode, source_ref: SourceReference, directly: bool=None) -> None:
        """
        Append an opcode to the instruction block of the current method.
        If directly is set to True, the instruction will not be written into the method-local buffer
        """
        if not source_ref:
            raise Exception('Cannot add instruction without a source ref')

        opcode.source_ref = source_ref

        if directly:
            self.instructions.append(opcode)
        else:
            self.instruction_block.append(opcode)

    def append_static(self, data: bytes) -> int:
        """
        Add a serialized blob of static data and return its index
        """

        self.data.append(data)
        return len(self.data) - 1

    def insert(self, index, buffer: 'CompilationContext'):
        """
        Insert a compilation context into this one at a given position
        """

        assert len(buffer.instructions) == 0
        assert len(buffer.instruction_block) == 1
        self.instruction_block.insert(index, buffer.instruction_block[0])

    def epilogue(self, buffer):
        """
        Appends an epilogue context into the pending buffer list
        """

        self.epilogues.append(buffer.instruction_block)

    def buffer(self) -> 'CompilationContext':
        """
        Create a new independent compilation context which can later be merged into the primary context
        """

        return CompilationContext(self.symbols, self.source)

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

    def method_start(self, method_locals, *args) -> None:
        """
        Mark the start of the method using a method definition Opcode.
        Additionally, updates the list of available locals, and flushes the instruction block.
        """

        self.current_locals = method_locals

        self.instruction_block = [
            SentinelMethodDefinition(*args)
        ]

    def method_end(self) -> None:
        """
        Mark the end of a method
        """

        self.instructions += self.instruction_block + collection_utils.flatten(self.epilogues) + [SentinelMethodEnd()]
        self.instruction_block = None

    def update_conditional_jumps(self) -> None:
        """
        Finalize a conditional jump in the stack of unresolved conditional jumps and pop it off.
        """

        for instruction, jump in list(self.conditional_groups[-1].items())[:-1]:
            jump.update(self.current_index())

        self.conditional_groups.pop()

    def bytes(self) -> bytes:
        """
        Serializes the compilation context into thinglang bytecode
        """

        instructions = self.instructions + [SentinelCodeEnd()]

        if not all(x.source_ref is not None for x in instructions):
            raise Exception('Not all instructions could be mapped to their source: {}'.format([x for x in instructions if x.source_ref is None]))

        code = bytes().join(x.resolve() for x in instructions)
        data = bytes().join(x for x in self.data) + SentinelDataEnd().resolve()
        source_map = bytes().join(x.source_ref.serialize() for x in instructions)

        header = bytes('THING', 'utf-8') + bytes([0xcc]) + struct.pack(HEADER_FORMAT, *BytecodeHeader(
            version=1,
            instruction_count=len(instructions),
            data_item_count=len(self.data),
            entrypoint=self.entry

        ))

        return header + code + data + source_map + bytes(self.source.raw_contents, 'utf-8')

    @property
    def last_instruction(self) -> Opcode:
        """
        Returns the last instruction added to the method-local buffer
        """
        return self.instruction_block[-1]
