from thinglang.compiler.opcodes import MEMBERS, METHODS, FRAME_SIZE, ARGUMENTS
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


class SentinelMethodDefinition(Opcode):
    """
    Signifies a method definition boundary.
    """
    ARGS = FRAME_SIZE, ARGUMENTS


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
