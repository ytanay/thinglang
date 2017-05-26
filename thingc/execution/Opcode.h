#pragma once

#include <string>

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

         default:
             return "Unknown opcode";
    }
}