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
    PUSH = 2,
    PUSH_STATIC = 3,
    PUSH_NULL = 4,
    POP = 5,
    SET = 6,
    SET_STATIC = 7,
    CALL = 8,
    CALL_INTERNAL = 9,
    RETURN = 10,
    INSTANTIATE = 11,
    INSTANTIATE_SET = 12,
    JUMP = 13,
    JUMP_CONDITIONAL = 14,
    THING_DEFINITION = 15,
    METHOD_DEFINITION = 16,
    METHOD_END = 17
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::INVALID:
            return "INVALID";

        case Opcode::PASS:
            return "PASS";

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

        case Opcode::CALL_INTERNAL:
            return "CALL_INTERNAL";

        case Opcode::RETURN:
            return "RETURN";

        case Opcode::INSTANTIATE:
            return "INSTANTIATE";

        case Opcode::INSTANTIATE_SET:
            return "INSTANTIATE_SET";

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

        case Opcode::PUSH:
            return 1;

        case Opcode::PUSH_STATIC:
            return 1;

        case Opcode::PUSH_NULL:
            return 0;

        case Opcode::POP:
            return 0;

        case Opcode::SET:
            return 1;

        case Opcode::SET_STATIC:
            return 2;

        case Opcode::CALL:
            return 2;

        case Opcode::CALL_INTERNAL:
            return 2;

        case Opcode::RETURN:
            return 0;

        case Opcode::INSTANTIATE:
            return 1;

        case Opcode::INSTANTIATE_SET:
            return 2;

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
