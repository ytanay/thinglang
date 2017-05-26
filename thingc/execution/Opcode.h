#pragma once

enum class Opcode {
	INVALID = 0,
	NOP = 1,
	
	PUSH = 2, // pushes a reference into the stack
	PUSH_STATIC = 3, // pushes static data into the stack
	POP = 4, // pop anything to void

	SET = 5, // pop a reference from the stack and assign it
	SET_STATIC = 6, // set a reference to static data

	CALL = 7,
	CALL_METHOD = 8,
	CALL_INTERNAL = 9,
	RETURN = 10,

	PRINT = 11,

    METHOD_END = 12
};
