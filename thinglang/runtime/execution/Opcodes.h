/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class Opcode {
    PUSH_MEMBER = 6,
    POP_MEMBER = 10,
    POP_DEREFERENCED = 11,
    CALL = 15,
    CALL_INTERNAL = 16,
    ELEMENT_REFERENCED = 0,
    PUSH_LOCAL = 5,
    POP_LOCAL = 9,
    ASSIGN_STATIC = 12,
    ASSIGN_LOCAL = 13,
    LOCAL_REFERENCED = 1,
    INVALID = 2,
    PASS = 3,
    PUSH_NULL = 4,
    PUSH_STATIC = 7,
    POP = 8,
    DEREFERENCE = 14,
    RETURN = 17,
    INSTANTIATE = 18,
    JUMP = 19,
    JUMP_CONDITIONAL = 20,
    THING_DEFINITION = 21,
    METHOD_DEFINITION = 22,
    METHOD_END = 23
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

        case Opcode::ELEMENT_REFERENCED:
            return "ELEMENT_REFERENCED";

        case Opcode::PUSH_LOCAL:
            return "PUSH_LOCAL";

        case Opcode::POP_LOCAL:
            return "POP_LOCAL";

        case Opcode::ASSIGN_STATIC:
            return "ASSIGN_STATIC";

        case Opcode::ASSIGN_LOCAL:
            return "ASSIGN_LOCAL";

        case Opcode::LOCAL_REFERENCED:
            return "LOCAL_REFERENCED";

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

        case Opcode::POP_MEMBER:
            return 2;

        case Opcode::POP_DEREFERENCED:
            return 1;

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

        case Opcode::ASSIGN_STATIC:
            return 2;

        case Opcode::ASSIGN_LOCAL:
            return 2;

        case Opcode::LOCAL_REFERENCED:
            return 0;

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
