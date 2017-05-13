#pragma once

#include <memory>

#include "Opcode.h"

class Symbol {

public:
	Symbol(Opcode opcode) : opcode(opcode) {};
	Symbol(Opcode opcode, unsigned int target) : opcode(opcode), target(target) {};

	void execute();

private:
	Opcode opcode;
	unsigned int target;
};
