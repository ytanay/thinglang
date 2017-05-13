#pragma once

enum class Opcode {
	INVALID = 0,
	NOP = 1,
	
	PUSH = 2,
	PUSH_CONST = 3,
	POP = 4,
	SET = 5,
	
	CALL = 6,
	CALL_METHOD = 7,
	CALL_INTERNAL = 8,
	RETURN = 9,

	PRINT = 10
};

