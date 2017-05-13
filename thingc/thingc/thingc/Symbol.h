#pragma once

#include "Opcode.h"
#include <memory>

class Symbol {

public:
	Symbol(Opcode opcode) : opcode(opcode) {};
	Symbol(Opcode opcode, unsigned int target) : opcode(opcode), target(target) {};

	void execute();

private:
	Opcode opcode;
	unsigned int target;
};
