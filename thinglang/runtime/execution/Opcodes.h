/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class Opcode {
    PUSH_MEMBER = 4,
    POP_MEMBER = 8,
    POP_DEREFERENCED = 9,
    CALL = 13,
    CALL_INTERNAL = 14,
    PUSH_LOCAL = 3,
    POP_LOCAL = 7,
    ASSIGN_STATIC = 10,
    ASSIGN_LOCAL = 11,
    INVALID = 0,
    PASS = 1,
    PUSH_NULL = 2,
    PUSH_STATIC = 5,
    POP = 6,
    DEREFERENCE = 12,
    RETURN = 15,
    INSTANTIATE = 16,
    JUMP = 17,
    JUMP_CONDITIONAL = 18,
    SENTINEL_THING_DEFINITION = 19,
    SENTINEL_METHOD_DEFINITION = 20,
    SENTINEL_METHOD_END = 21,
    SENTINEL_CODE_END = 22,
    SENTINEL_DATA_END = 23
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::PUSH_MEMBER:
            return "PUSH_MEMBER";

        case Opcode::POP_MEMBER:
            return "POP_MEMBER";

        case Opcode::POP_DEREFERENCED:
            return "POP_DEREFERENCED";

        case Opcode::CALL:
            return "CALL";

        case Opcode::CALL_INTERNAL:
            return "CALL_INTERNAL";

        case Opcode::PUSH_LOCAL:
            return "PUSH_LOCAL";

        case Opcode::POP_LOCAL:
            return "POP_LOCAL";

        case Opcode::ASSIGN_STATIC:
            return "ASSIGN_STATIC";

        case Opcode::ASSIGN_LOCAL:
            return "ASSIGN_LOCAL";

        case Opcode::INVALID:
            return "INVALID";

        case Opcode::PASS:
            return "PASS";

        case Opcode::PUSH_NULL:
            return "PUSH_NULL";

        case Opcode::PUSH_STATIC:
            return "PUSH_STATIC";

        case Opcode::POP:
            return "POP";

        case Opcode::DEREFERENCE:
            return "DEREFERENCE";

        case Opcode::RETURN:
            return "RETURN";

        case Opcode::INSTANTIATE:
            return "INSTANTIATE";

        case Opcode::JUMP:
            return "JUMP";

        case Opcode::JUMP_CONDITIONAL:
            return "JUMP_CONDITIONAL";

        case Opcode::SENTINEL_THING_DEFINITION:
            return "SENTINEL_THING_DEFINITION";

        case Opcode::SENTINEL_METHOD_DEFINITION:
            return "SENTINEL_METHOD_DEFINITION";

        case Opcode::SENTINEL_METHOD_END:
            return "SENTINEL_METHOD_END";

        case Opcode::SENTINEL_CODE_END:
            return "SENTINEL_CODE_END";

        case Opcode::SENTINEL_DATA_END:
            return "SENTINEL_DATA_END";
    }
}

inline auto arg_count(Opcode val){
    switch (val){
        
        case Opcode::PUSH_MEMBER:
            return 2;

        case Opcode::POP_MEMBER:
            return 2;

        case Opcode::POP_DEREFERENCED:
            return 1;

        case Opcode::CALL:
            return 2;

        case Opcode::CALL_INTERNAL:
            return 2;

        case Opcode::PUSH_LOCAL:
            return 1;

        case Opcode::POP_LOCAL:
            return 1;

        case Opcode::ASSIGN_STATIC:
            return 2;

        case Opcode::ASSIGN_LOCAL:
            return 2;

        case Opcode::INVALID:
            return 0;

        case Opcode::PASS:
            return 0;

        case Opcode::PUSH_NULL:
            return 0;

        case Opcode::PUSH_STATIC:
            return 1;

        case Opcode::POP:
            return 0;

        case Opcode::DEREFERENCE:
            return 1;

        case Opcode::RETURN:
            return 0;

        case Opcode::INSTANTIATE:
            return 1;

        case Opcode::JUMP:
            return 1;

        case Opcode::JUMP_CONDITIONAL:
            return 1;

        case Opcode::SENTINEL_THING_DEFINITION:
            return 2;

        case Opcode::SENTINEL_METHOD_DEFINITION:
            return 2;

        case Opcode::SENTINEL_METHOD_END:
            return 0;

        case Opcode::SENTINEL_CODE_END:
            return 0;

        case Opcode::SENTINEL_DATA_END:
            return 0;
    }
}
