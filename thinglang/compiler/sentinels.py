from thinglang.compiler.opcodes import Opcode
from thinglang.compiler.opcodes import MEMBERS, METHODS, FRAME_SIZE, ARGUMENTS

# Sentinels and file boundaries


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