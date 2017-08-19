import struct

import itertools

import collections

from thinglang.utils import collection_utils
from thinglang.utils.describable import camelcase_to_underscore

STATIC_ID = LOCAL_ID = MEMBER_ID = SOURCE = FRAME_SIZE = ARGUMENTS = MEMBERS = METHODS = IDX = TYPE_ID = METHOD_ID = TARGET = ID = object()

OpcodeDescription = collections.namedtuple('OpcodeDescription', ['name', 'opcode', 'arg_count'])


class OpcodeRegistration(type):
    COUNT = itertools.count(-1)

    def __new__(mcs, name, bases, dct):
        mcs = super(OpcodeRegistration, mcs).__new__(mcs, name, bases, dct)
        assert name.startswith('Opcode')
        mcs.OPCODE = next(OpcodeRegistration.COUNT)
        return mcs


class Opcode(object, metaclass=OpcodeRegistration):
    ARGS = ()
    OPCODE = -1

    def __init__(self, *args):
        super(Opcode, self).__init__()
        self.args = args

    def update(self, *args):
        self.args = args

    def resolve(self):
        assert len(self.args) == len(self.ARGS), 'Mismatched argument count. Expected {}, got {}'.format(len(self.ARGS), len(self.args))
        assert all(isinstance(x, int) for x in self.args), 'Incorrect argument types: {}'.format(self.args)
        return struct.pack(self.format_string(), self.OPCODE, *self.args)

    @classmethod
    def format_string(cls):
        return '<B{}'.format('I' * len(cls.ARGS))

    @classmethod
    def all(cls):
        return [
            OpcodeDescription(opcode.name(), opcode.OPCODE, len(opcode.ARGS)) for opcode in collection_utils.subclasses(cls)
        ]

    @classmethod
    def name(cls):
        return camelcase_to_underscore(cls.__name__.replace('Opcode', ''))

    def __eq__(self, other):
        return type(self) == type(other) and self.args == other.args

    def __str__(self):
        return '{}({})'.format(type(self).__name__, self.args)

    def __repr__(self):
        return str(self)

class OpcodeElementReferenced(Opcode):

    @classmethod
    def type_reference(cls, element_ref):
        return cls(element_ref.thing_index, element_ref.element_index)

    @classmethod
    def local_reference(cls, element_ref):
        return cls(element_ref.local_index, element_ref.element_index)


class OpcodeLocalReferenced(Opcode):

    @classmethod
    def from_reference(cls, local_ref, *args):
        return cls(local_ref.local_index, *args)

    @classmethod
    def from_references(cls, destination_ref, source_ref):
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


class OpcodePushLocal(OpcodeLocalReferenced):
    """
    Push a reference to a local object from the stack frame into the program stack
    """
    ARGS = LOCAL_ID,


class OpcodePushMember(OpcodeElementReferenced):
    """
    Push a reference to a member from a local object on the stack frame into the program stack
    """
    ARGS = LOCAL_ID, MEMBER_ID


class OpcodePushStatic(Opcode):
    """
    Push a reference to an object from the static segment into the program stack
    """
    ARGS = STATIC_ID,


# Stack pop operations

class OpcodePop(Opcode):
    """
    Pops a reference from the program stack into nothing
    """
    pass


class OpcodePopLocal(OpcodeLocalReferenced):
    """
    Pops a reference from the program stack into a local object
    """
    ARGS = LOCAL_ID,


class OpcodePopMember(OpcodeElementReferenced):
    """
    Sets a reference frm the stack into a member of a local object
    """
    ARGS = LOCAL_ID, MEMBER_ID


class OpcodePopDereferenced(OpcodeElementReferenced):
    """
    Sets a reference from the stack into a dereferenced member on the stack
    """
    ARGS = MEMBER_ID,


# Assignment operations

class OpcodeAssignStatic(OpcodeLocalReferenced):
    """
    Sets a reference from the static segment into the stack frame
    """
    ARGS = LOCAL_ID, STATIC_ID


class OpcodeAssignLocal(OpcodeLocalReferenced):
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

class OpcodeCall(OpcodeElementReferenced):
    """
    Calls a user defined method
    """
    ARGS = TYPE_ID, METHOD_ID


class OpcodeCallInternal(OpcodeElementReferenced):
    """
    Calls a native (compiled) method
    """
    ARGS = TYPE_ID, METHOD_ID


class OpcodeReturn(Opcode):
    """
    Returns to the calling method
    """
    pass


class OpcodeInstantiate(Opcode):
    """
    Create a reference container to a new thing instance and pushes it to the program stack
    """
    ARGS = TYPE_ID,


class OpcodeJump(Opcode):
    """
    Jumps to an absolute instruction in the current method
    """
    ARGS = IDX,


class OpcodeJumpConditional(Opcode):
    """
    Pops a reference from the stack and evaluates it.
    If it evaluates to true, jumps to an absolute instruction in the current method
    """
    ARGS = IDX,


class OpcodeThingDefinition(Opcode):
    """
    Signifies a thing definition boundary.
    Used as a sentinel during bytecode parsing
    """
    ARGS = MEMBERS, METHODS


class OpcodeMethodDefinition(Opcode):
    """
    Signifies a method definition boundary.
    Used as a sentinel during bytecode parsing
    """
    ARGS = FRAME_SIZE, ARGUMENTS


class OpcodeMethodEnd(Opcode):
    """
    Signifies a method boundary.
    Used as a sentinel during bytecode parsing
    """
    pass

