import collections
import struct

from thinglang.compiler.opcodes import OpcodeHandlerDescription, OpcodeHandlerRangeDefinition
from thinglang.compiler.sentinels import SentinelMethodDefinition, SentinelCodeEnd, SentinelDataEnd
from thinglang.utils.source_context import SourceContext

HEADER_FORMAT = '<HIIII'
BytecodeHeader = collections.namedtuple('BytecodeHeader', [
    'version',
    'instruction_count',
    'data_item_count',
    'entrypoint',
    'initial_frame_size'
])


class CompilationContext(object):
    """
    The CompilationContext classes manages the entire compilation pass, including serialization into bytecode
    """
    def __init__(self, symbols, source: SourceContext, entry=None):

        self.symbols = symbols
        self.source = source

        self.current_locals = None
        self.entry = entry or 0

        self.methods = {}

    def add(self, method_id, method, buffer):
        """
        Add a compiled method buffer
        """

        self.methods[method_id] = method, buffer

    def buffer(self) -> 'CompilationContext':
        """
        Create a new independent compilation context which can later be merged into the primary context
        """

        return CompilationContext(self.symbols, self.source)

    def bytes(self) -> bytes:
        """
        Serializes the compilation context into thinglang bytecode
        """

        instructions = []
        data_items = []
        offsets = {}

        for method_idx, (method, buffer) in self.methods.items():
            instructions.append(SentinelMethodDefinition(0, 0))

            method_offset, data_offset = len(instructions) + len(buffer.exception_table) * 2, len(data_items)

            # First, we write the exception table for this method
            for exception, handler, start_index, end_index in buffer.exception_table:
                instructions.append(OpcodeHandlerDescription(method_offset + len(buffer.instructions) + handler, exception))
                instructions.append(OpcodeHandlerRangeDefinition(start_index + method_offset, end_index + method_offset))

            offsets[method_idx] = method_offset, method.frame_size
            instructions.extend(instruction.update_offset(method_offset, data_offset) for instruction in buffer.instructions)
            instructions.extend(instruction.update_offset(method_offset, data_offset) for instruction in buffer.epilogues)

            data_items.extend(buffer.data)

        for instruction in instructions:
            instruction.update_references(offsets)

        instructions.append(SentinelCodeEnd())

        if not all(x.source_ref is not None for x in instructions):
            raise Exception('Not all instructions could be mapped to their source: {}'.format([x for x in instructions if x.source_ref is None]))

        code = bytes().join(x.serialize() for x in instructions)
        data = bytes().join(x for x in data_items) + SentinelDataEnd().serialize()
        source_map = bytes().join(x.source_ref.serialize() for x in instructions)

        header = bytes('THING', 'utf-8') + bytes([0xcc]) + struct.pack(HEADER_FORMAT, *BytecodeHeader(
            version=2,
            instruction_count=len(instructions),
            data_item_count=len(data_items),
            entrypoint=offsets[(self.entry, 0)][0],
            initial_frame_size=offsets[(self.entry, 0)][1]
        ))

        return header + code + data + source_map + bytes(self.source.raw_contents, 'utf-8')


