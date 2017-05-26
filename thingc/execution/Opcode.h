#pragma once

#include <string>

enum class Opcode {
	INVALID = 0,
	NOP = 1,
	
	PUSH = 2, // pushes a reference into the stack
	PUSH_STATIC = 3, // pushes static data into the stack
    PUSH_NULL = 4,

	POP = 5, // pop anything to void

	SET = 6, // pop a reference from the stack and assign it
	SET_STATIC = 7, // set a reference to static data

	CALL = 8,
	CALL_METHOD = 9,
	CALL_INTERNAL = 10,
	RETURN = 11,

    JUMP = 12,
    CONDITIONAL_JUMP = 13,

	PRINT = 14,

    METHOD_END = 15
};

inline std::string describe(Opcode o){
     switch (o){
         case Opcode::INVALID:
             return "INVALID";
         case Opcode::NOP:
             return "NOP";

         case Opcode::PUSH:
             return "PUSH";
         case Opcode::PUSH_STATIC:
             return "PUSH_STATIC";

         case Opcode::PUSH_NULL:
             return "PUSH_NULL";

         case Opcode::POP:
             return "POP";

         case Opcode::SET:
             return "SET";

         case Opcode::SET_STATIC:
             return "SET_STATIC";

         case Opcode::CALL:
             return "CALL";
         case Opcode::CALL_METHOD:
             return "CALL_METHOD";
         case Opcode::CALL_INTERNAL:
             return "CALL_INTERNAL";

         case Opcode::RETURN:
             return "RETURN";
         case Opcode::PRINT:
             return "PRINT";

         case Opcode::JUMP:
             return "JUMP";
         case Opcode::CONDITIONAL_JUMP:
             return "CONDITIONAL_JUMP";

         default:
             return "Unknown opcode";
    }
}