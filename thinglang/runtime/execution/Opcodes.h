/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class Opcode {
    PUSH_MEMBER = 5,
    SET_MEMBER = 11,
    CALL = 13,
    CALL_INTERNAL = 14,
    ELEMENT_REFERENCED = 0,
    PUSH_LOCAL = 4,
    POP_LOCAL = 9,
    SET_LOCAL_STATIC = 10,
    LOCAL_REFERENCED = 1,
    INVALID = 2,
    PASS = 3,
    PUSH_STATIC = 6,
    PUSH_NULL = 7,
    POP = 8,
    RESOLVE = 12,
    RETURN = 15,
    INSTANTIATE = 16,
    JUMP = 17,
    JUMP_CONDITIONAL = 18,
    THING_DEFINITION = 19,
    METHOD_DEFINITION = 20,
    METHOD_END = 21
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::PUSH_MEMBER:
            return "PUSH_MEMBER";

        case Opcode::SET_MEMBER:
            return "SET_MEMBER";

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

        case Opcode::SET_LOCAL_STATIC:
            return "SET_LOCAL_STATIC";

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
        
        case Opcode::PUSH_MEMBER:
            return 2;

        case Opcode::SET_MEMBER:
            return 2;

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

        case Opcode::SET_LOCAL_STATIC:
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
