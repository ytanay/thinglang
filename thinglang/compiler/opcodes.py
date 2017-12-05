import collections
import itertools
import struct
from typing import List

from thinglang.compiler.references import ElementReference, LocalReference
from thinglang.utils import collection_utils
from thinglang.utils.logging_utils import camelcase_to_underscore
from thinglang.utils.source_context import SourceReference

STATIC_ID = LOCAL_ID = MEMBER_ID = SOURCE = FRAME_SIZE = ARGUMENTS = MEMBERS = METHODS = TYPE_ID = METHOD_ID = TARGET = ID = INDEX = object()
INSTRUCTION_INDEX = object()

OpcodeDescription = collections.namedtuple('OpcodeDescription', ['name', 'opcode', 'arg_count'])


class OpcodeRegistration(type):
    """
    This metaclass gives every opcode an actual numeric code, for use in the bytecode.
    """
    COUNT = itertools.count(-1)

    def __new__(mcs, name, bases, dct):
        mcs = super(OpcodeRegistration, mcs).__new__(mcs, name, bases, dct)
        if name.startswith('Opcode') or name.startswith('Sentinel'):
            mcs.OPCODE = next(OpcodeRegistration.COUNT)
        return mcs


class Opcode(object, metaclass=OpcodeRegistration):
    """
    Describes an instruction in the thinglang assembly language.

    An instance of this class contains an opcode and its operands (i.e. arguments). The operands are not necessarily
    known when the class is instantiated, but must be resolved before the opcode is serialized into bytecode.
    """

    ARGS = ()
    OPCODE = -1

    def __init__(self, *args, source_ref=SourceReference.invalid()):
        super(Opcode, self).__init__()
        self.args = args
        self.source_ref = source_ref

    def update(self, *args) -> None:
        """
        Update the instruction's arguments
        """
        self.args = args

    def update_offset(self, method_offset: int, data_offset: int, relative: bool=False):
        return self

    def update_references(self, offsets):
        pass

    def serialize(self) -> bytes:
        """
        Validates this instruction and convert it to binary bytecode
        """
        if len(self.args) != len(self.ARGS):
            raise ValueError('Mismatched argument count. Expected {}, got {}'.format(len(self.ARGS), len(self.args)))

        if not all(isinstance(x, int) for x in self.args):
            raise TypeError('Incorrect argument types: {}'.format(self.args))

        return struct.pack(self.format_string(), self.OPCODE, *self.args)

    @classmethod
    def format_string(cls) -> str:
        """
        Generates the formating string used when this opcode is serialized.
        Assumes all operands are unsigned 32-bit integers
        """
        return '<B{}'.format('I' * len(cls.ARGS))

    @classmethod
    def all(cls) -> List[OpcodeDescription]:
        """
        Returns a list of all opcodes deriving from this class
        """
        return [
            OpcodeDescription(opcode.name(), opcode.OPCODE, len(opcode.ARGS))
            for opcode in collection_utils.subclasses(cls) if opcode.executable()
        ]

    @classmethod
    def name(cls) -> str:
        """
        Returns the canonical name of this opcode
        """
        return camelcase_to_underscore(cls.__name__.replace('Opcode', ''))

    @classmethod
    def executable(cls) -> bool:
        """
        Returns whether this is a real executable opcode (e.g. opcode leaf) or a base class
        """
        return cls is not Opcode and (cls.__name__.startswith('Opcode') or cls.__name__.startswith('Sentinel'))

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.args == other.args

    def __str__(self) -> str:
        return '{}({})'.format(type(self).__name__, self.args)


class ElementReferenced(Opcode):

    @classmethod
    def from_reference(cls, ref: ElementReference):
        """
        Automatically construct an appropriate opcode instance using a a given element reference
        """
        return cls.local_reference(ref) if ref.is_local else cls.type_reference(ref)

    @classmethod
    def type_reference(cls, element_ref: ElementReference):
        """
        Generate a type-referencing opcode
        """
        return cls(element_ref.thing_index, element_ref.element_index)

    @classmethod
    def local_reference(cls, element_ref: ElementReference):
        """
        Generate a locally-referencing opcode.
        """
        return cls(element_ref.local_index, element_ref.element_index)


class LocalReferenced(Opcode):

    @classmethod
    def from_reference(cls, local_ref: LocalReference, *args):
        """
        Create a locally referencing opcode
        """
        return cls(local_ref.local_index, *args)

    @classmethod
    def from_references(cls, destination_ref: LocalReference, source_ref):
        """
        Create a source->destination locally-referencing opcode instance
        """
        return cls(destination_ref.local_index, source_ref.local_index)


class OpcodeInvalid(Opcode):
    """
    Sanity trap for broken bytecode
    """
    pass


class OpcodePass(Opcode):
    """
    A good old fashioned NO-OP
    """
    pass


# Stack push operations

class OpcodePushNull(Opcode):
    """
    Push a null reference into the program stack
    """
    pass


class OpcodePushLocal(LocalReferenced):
    """
    Push a reference to a local object from the stack frame into the program stack
    """
    ARGS = LOCAL_ID,


class OpcodePushMember(ElementReferenced):
    """
    Push a reference to a member from a local object on the stack frame into the program stack
    """
    ARGS = LOCAL_ID, MEMBER_ID


class OpcodePushStatic(Opcode):
    """
    Push a reference to an object from the static segment into the program stack
    """
    ARGS = STATIC_ID,

    def update_offset(self, method_offset: int, data_offset: int, relative: bool=False):
        self.args = self.args[0] + data_offset,
        return self


class OpcodePushIndex(Opcode):
    """
    Pop an index and value from the stack and push the value at the index provided
    """


class OpcodePushIndexImmediate(Opcode):
    """
    Pop a value from the stack and push the value at the immediate index provided
    """
    ARGS = INDEX,


# Stack pop operations

class OpcodePop(Opcode):
    """
    Pops a reference from the program stack into nothing
    """
    pass


class OpcodePopLocal(LocalReferenced):
    """
    Pops a reference from the program stack into a local object
    """
    ARGS = LOCAL_ID,


class OpcodePopMember(ElementReferenced):
    """
    Sets a reference frm the stack into a member of a local object
    """
    ARGS = LOCAL_ID, MEMBER_ID


class OpcodePopDereferenced(ElementReferenced):
    """
    Sets a reference from the stack into a dereferenced member on the stack
    """
    ARGS = MEMBER_ID,


class OpcodeArgCopy(Opcode):

    ARGS = ARGUMENTS,


# Assignment operations

class OpcodeAssignStatic(LocalReferenced):
    """
    Sets a reference from the static segment into the stack frame
    """
    ARGS = LOCAL_ID, STATIC_ID

    def update_offset(self, method_offset: int, data_offset: int):
        self.args = self.args[0], self.args[1] + data_offset
        return self


class OpcodeAssignLocal(LocalReferenced):
    """
    Overrides a local object with a reference to another local object
    """
    ARGS = LOCAL_ID, LOCAL_ID


# Dereference operations

class OpcodeDereference(Opcode):
    """
    Pops a reference from the program stack, resolves a member in it, and pushes the result back into the stack
    """
    ARGS = MEMBER_ID,


# Method Calls

class OpcodeCall(ElementReferenced):
    """
    Calls a user defined method
    """
    ARGS = INSTRUCTION_INDEX, FRAME_SIZE

    def update_references(self, offsets):
        self.args = offsets[self.args]


class OpcodeCallInternal(ElementReferenced):
    """
    Calls a native (compiled) method
    """
    ARGS = TYPE_ID, METHOD_ID


class OpcodeReturn(Opcode):
    """
    Returns to the calling method
    """
    pass


class OpcodeThrow(Opcode):
    """
    Throws an exception instance on the stack
    """
    ARGS = TYPE_ID,


class OpcodeInstantiate(Opcode):
    """
    Create a reference container to a new thing instance and pushes it to the program stack
    """
    ARGS = ARGUMENTS, ARGUMENTS


class OpcodeJump(Opcode):
    """
    Jumps to an absolute instruction in the current method
    """
    ARGS = INSTRUCTION_INDEX,

    def __init__(self, *args, absolute=False):
        super(OpcodeJump, self).__init__(*args)
        self.absolute = absolute

    def update_offset(self, method_offset: int, data_offset: int, relative: bool=False):
        if not relative:
            self.args = self.args[0] + method_offset,
        return self


class OpcodeJumpConditional(OpcodeJump):
    """
    Pops a reference from the stack and evaluates it.
    If it evaluates to true, jumps to an absolute instruction in the current method
    """
    ARGS = INSTRUCTION_INDEX,


# Exception handling

class OpcodeHandlerDescription(Opcode):
    """
    Defines an exception
    """
    ARGS = INSTRUCTION_INDEX, INSTRUCTION_INDEX


class OpcodeHandlerRangeDefinition(Opcode):
    """
    Defines the PC range for the following exception handler
    """
    ARGS = TYPE_ID, INSTRUCTION_INDEX


