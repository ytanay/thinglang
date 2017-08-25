#pragma once

#include <memory>

#include "../utils/TypeNames.h"
#include "Opcodes.h"

class Symbol {

public:
    explicit Symbol(Opcode opcode) : opcode(opcode) {};

    Symbol(Opcode opcode, Index target) : opcode(opcode), target(target) {};

    Symbol(Opcode opcode, Index target, Index secondary) : opcode(opcode), target(target),
                                                                         secondary(secondary) {};

    Opcode opcode = Opcode::INVALID;
    Index target = 0;
    Index secondary = 0;
};
