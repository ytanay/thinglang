/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class Opcode {
    INVALID = 0,
    PASS = 1,
    PUSH_LOCAL = 2,
    PUSH_STATIC = 3,
    PUSH_NULL = 4,
    POP = 5,
    POP_LOCAL = 6,
    SET_LOCAL = 7,
    SET_MEMBER = 8,
    RESOLVE = 9,
    CALL = 10,
    CALL_INTERNAL = 11,
    RETURN = 12,
    INSTANTIATE = 13,
    JUMP = 14,
    JUMP_CONDITIONAL = 15,
    THING_DEFINITION = 16,
    METHOD_DEFINITION = 17,
    METHOD_END = 18
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::INVALID:
            return "INVALID";

        case Opcode::PASS:
            return "PASS";

        case Opcode::PUSH_LOCAL:
            return "PUSH_LOCAL";

        case Opcode::PUSH_STATIC:
            return "PUSH_STATIC";

        case Opcode::PUSH_NULL:
            return "PUSH_NULL";

        case Opcode::POP:
            return "POP";

        case Opcode::POP_LOCAL:
            return "POP_LOCAL";

        case Opcode::SET_LOCAL:
            return "SET_LOCAL";

        case Opcode::SET_MEMBER:
            return "SET_MEMBER";

        case Opcode::RESOLVE:
            return "RESOLVE";

        case Opcode::CALL:
            return "CALL";

        case Opcode::CALL_INTERNAL:
            return "CALL_INTERNAL";

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
        
        case Opcode::INVALID:
            return 0;

        case Opcode::PASS:
            return 0;

        case Opcode::PUSH_LOCAL:
            return 1;

        case Opcode::PUSH_STATIC:
            return 1;

        case Opcode::PUSH_NULL:
            return 0;

        case Opcode::POP:
            return 0;

        case Opcode::POP_LOCAL:
            return 1;

        case Opcode::SET_LOCAL:
            return 2;

        case Opcode::SET_MEMBER:
            return 2;

        case Opcode::RESOLVE:
            return 1;

        case Opcode::CALL:
            return 2;

        case Opcode::CALL_INTERNAL:
            return 2;

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
