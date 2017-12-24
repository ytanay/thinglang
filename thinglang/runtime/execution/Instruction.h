#pragma once

#include "Opcodes.h"
#include "../utils/TypeNames.h"

class Instruction {

public:
    Instruction(Index index, Opcode opcode) : index(index), opcode(opcode) {};

    Instruction(Index index, Opcode opcode, Index target) : index(index), opcode(opcode), target(target) {};

    Instruction(Index index, Opcode opcode, Index target, Index secondary) : index(index), opcode(opcode),
                                                                             target(target), secondary(secondary) {};

    Opcode opcode = Opcode::INVALID;
    Index target = 0;
    Index secondary = 0;
    Index index = 0;
};
