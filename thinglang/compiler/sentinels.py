from thinglang.compiler.opcodes import MEMBERS, METHODS, FRAME_SIZE, ARGUMENTS, TARGET, TYPE_ID
from thinglang.compiler.opcodes import Opcode


class SentinelImportTableEntry(Opcode):
    """
    Signifies an import table entry
    """


class SentinelImportTableEnd(Opcode):
    """
    Signifies the end of the import table
    """


class SentinelThingDefinition(Opcode):
    """
    Signifies the start of thing definition
    """
    ARGS = MEMBERS, METHODS


class SentinelThingExtends(Opcode):
    """
    Signifies that the thing definition being declared extends a previous thing definition
    """
    ARGS = TYPE_ID,


class SentinelMethodDefinition(Opcode):
    """
    Signifies a method definition boundary.
    """
    ARGS = TARGET, FRAME_SIZE


class SentinelMethodEnd(Opcode):
    """
    Signifies a method boundary.
    """
    pass


class SentinelCodeEnd(Opcode):
    """
    Signifies the code section boundary.
    """
    pass


class SentinelDataEnd(Opcode):
    """
    Signifies the code section boundary.
    """
    pass
