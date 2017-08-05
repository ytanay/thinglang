import struct

import itertools

import collections

from thinglang.utils import collection_utils
from thinglang.utils.describable import camelcase_to_underscore

MEMBER_ID = SOURCE = FRAME_SIZE = ARGUMENTS = MEMBERS = METHODS = IDX = TYPE_ID = METHOD_ID = TARGET = ID = object()

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


class OpcodeElementReferenced(Opcode):

    def __init__(self, element_ref):
        super().__init__(element_ref.thing_index, element_ref.element_index)


class OpcodeLocalReferenced(Opcode):

    def __init__(self, local_ref, *args):
        super().__init__(local_ref.local_index, *args)


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


class OpcodePushLocal(OpcodeLocalReferenced):
    """
    Push a reference to an object from the stack frame into the program stack
    """
    ARGS = ID,


class OpcodePushMember(OpcodeElementReferenced):
    """
    Push a reference to an object member from the stack frame into the program stack
    """
    ARGS = ID, ID


class OpcodePushStatic(Opcode):
    """
    Push a reference to an object from the static segment into the program stack
    """
    ARGS = ID,


class OpcodePushNull(Opcode):
    """
    Push a null reference into the program stack
    """
    pass


class OpcodePop(Opcode):
    """
    Pops a reference from the program stack into nothing
    """
    pass


class OpcodePopLocal(OpcodeLocalReferenced):
    """
    Pops a reference from the program stack into the stack frame
    """
    ARGS = TARGET,


class OpcodeSetLocalStatic(OpcodeLocalReferenced):
    """
    Sets a reference from the static segment into the stack frame
    """
    ARGS = TARGET, ID


class OpcodeSetMember(OpcodeElementReferenced):
    """
    Sets a reference frm the stack into a member
    """
    ARGS = TARGET, ID


class OpcodeResolve(Opcode):
    """
    Pops a reference from the program stack, resolves a member in it, and pushes the result back into the stack
    """
    ARGS = ID,


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

