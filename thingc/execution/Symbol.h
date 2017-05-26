#pragma once

#include <memory>

#include "Opcode.h"

class Symbol {

public:
	Symbol(Opcode opcode) : opcode(opcode) {};
	Symbol(Opcode opcode, unsigned int target) : opcode(opcode), target(target) {};
    Symbol(Opcode opcode, unsigned int target, unsigned int secondary) : opcode(opcode), target(target), secondary(secondary) {};


    void execute();

private:
	Opcode opcode;
	unsigned int target = 0;
    unsigned int secondary = 0;
};