/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class Opcode {
    CALL = 12,
    CALL_INTERNAL = 13,
    ELEMENT_REFERENCED = 0,
    PUSH_LOCAL = 4,
    POP_LOCAL = 8,
    SET_LOCAL = 9,
    LOCAL_REFERENCED = 1,
    INVALID = 2,
    PASS = 3,
    PUSH_STATIC = 5,
    PUSH_NULL = 6,
    POP = 7,
    SET_MEMBER = 10,
    RESOLVE = 11,
    RETURN = 14,
    INSTANTIATE = 15,
    JUMP = 16,
    JUMP_CONDITIONAL = 17,
    THING_DEFINITION = 18,
    METHOD_DEFINITION = 19,
    METHOD_END = 20
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::CALL:
            return "CALL";

        case Opcode::CALL_INTERNAL:
            return "CALL_INTERNAL";

        case Opcode::ELEMENT_REFERENCED:
            return "ELEMENT_REFERENCED";

        case Opcode::PUSH_LOCAL:
            return "PUSH_LOCAL";

        case Opcode::POP_LOCAL:
            return "POP_LOCAL";

        case Opcode::SET_LOCAL:
            return "SET_LOCAL";

        case Opcode::LOCAL_REFERENCED:
            return "LOCAL_REFERENCED";

        case Opcode::INVALID:
            return "INVALID";

        case Opcode::PASS:
            return "PASS";

        case Opcode::PUSH_STATIC:
            return "PUSH_STATIC";

        case Opcode::PUSH_NULL:
            return "PUSH_NULL";

        case Opcode::POP:
            return "POP";

        case Opcode::SET_MEMBER:
            return "SET_MEMBER";

        case Opcode::RESOLVE:
            return "RESOLVE";

        case Opcode::RETURN:
            return "RETURN";

        case Opcode::INSTANTIATE:
            return "INSTANTIATE";

        case Opcode::JUMP:
            return "JUMP";

        case Opcode::JUMP_CONDITIONAL:
            return "JUMP_CONDITIONAL";

        case Opcode::THING_DEFINITION:
            return "THING_DEFINITION";

        case Opcode::METHOD_DEFINITION:
            return "METHOD_DEFINITION";

        case Opcode::METHOD_END:
            return "METHOD_END";
        
        default:
            throw RuntimeError("Unrecognized Opcode in describe");
    }
}

inline auto arg_count(Opcode val){
    switch (val){
        
        case Opcode::CALL:
            return 2;

        case Opcode::CALL_INTERNAL:
            return 2;

        case Opcode::ELEMENT_REFERENCED:
            return 0;

        case Opcode::PUSH_LOCAL:
            return 1;

        case Opcode::POP_LOCAL:
            return 1;

        case Opcode::SET_LOCAL:
            return 2;

        case Opcode::LOCAL_REFERENCED:
            return 0;

        case Opcode::INVALID:
            return 0;

        case Opcode::PASS:
            return 0;

        case Opcode::PUSH_STATIC:
            return 1;

        case Opcode::PUSH_NULL:
            return 0;

        case Opcode::POP:
            return 0;

        case Opcode::SET_MEMBER:
            return 2;

        case Opcode::RESOLVE:
            return 1;

        case Opcode::RETURN:
            return 0;

        case Opcode::INSTANTIATE:
            return 1;

        case Opcode::JUMP:
            return 1;

        case Opcode::JUMP_CONDITIONAL:
            return 1;

        case Opcode::THING_DEFINITION:
            return 2;

        case Opcode::METHOD_DEFINITION:
            return 2;

        case Opcode::METHOD_END:
            return 0;
        
        default:
            throw RuntimeError("Unrecognized Opcode in arg_count");
    }
}
