/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include <string>



enum class Opcode {
    PUSH_MEMBER = 4,
    POP_MEMBER = 8,
    POP_DEREFERENCED = 9,
    CALL_STATIC = 15,
    CALL = 14,
    CALL_INTERNAL = 16,
    CALL_VIRTUAL = 17,
    PUSH_LOCAL = 3,
    POP_LOCAL = 7,
    ASSIGN_STATIC = 11,
    ASSIGN_LOCAL = 12,
    INVALID = 0,
    PASS = 1,
    PUSH_NULL = 2,
    PUSH_STATIC = 5,
    POP = 6,
    ARG_COPY = 10,
    DEREFERENCE = 13,
    RETURN = 18,
    THROW = 19,
    INSTANTIATE = 20,
    JUMP_CONDITIONAL = 22,
    JUMP = 21,
    HANDLER_DESCRIPTION = 23,
    HANDLER_RANGE_DEFINITION = 24,
    SENTINEL_IMPORT_TABLE_ENTRY = 25,
    SENTINEL_IMPORT_TABLE_END = 26,
    SENTINEL_THING_DEFINITION = 27,
    SENTINEL_THING_EXTENDS = 28,
    SENTINEL_METHOD_DEFINITION = 29,
    SENTINEL_METHOD_END = 30,
    SENTINEL_CODE_END = 31,
    SENTINEL_DATA_END = 32
};


inline auto describe(Opcode val){
    switch (val){
        
        case Opcode::PUSH_MEMBER:
            return "PUSH_MEMBER";

        case Opcode::POP_MEMBER:
            return "POP_MEMBER";

        case Opcode::POP_DEREFERENCED:
            return "POP_DEREFERENCED";

        case Opcode::CALL_STATIC:
            return "CALL_STATIC";

        case Opcode::CALL:
            return "CALL";

        case Opcode::CALL_INTERNAL:
            return "CALL_INTERNAL";

        case Opcode::CALL_VIRTUAL:
            return "CALL_VIRTUAL";

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

        case Opcode::ARG_COPY:
            return "ARG_COPY";

        case Opcode::DEREFERENCE:
            return "DEREFERENCE";

        case Opcode::RETURN:
            return "RETURN";

        case Opcode::THROW:
            return "THROW";

        case Opcode::INSTANTIATE:
            return "INSTANTIATE";

        case Opcode::JUMP_CONDITIONAL:
            return "JUMP_CONDITIONAL";

        case Opcode::JUMP:
            return "JUMP";

        case Opcode::HANDLER_DESCRIPTION:
            return "HANDLER_DESCRIPTION";

        case Opcode::HANDLER_RANGE_DEFINITION:
            return "HANDLER_RANGE_DEFINITION";

        case Opcode::SENTINEL_IMPORT_TABLE_ENTRY:
            return "SENTINEL_IMPORT_TABLE_ENTRY";

        case Opcode::SENTINEL_IMPORT_TABLE_END:
            return "SENTINEL_IMPORT_TABLE_END";

        case Opcode::SENTINEL_THING_DEFINITION:
            return "SENTINEL_THING_DEFINITION";

        case Opcode::SENTINEL_THING_EXTENDS:
            return "SENTINEL_THING_EXTENDS";

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

        case Opcode::CALL_STATIC:
            return 2;

        case Opcode::CALL:
            return 2;

        case Opcode::CALL_INTERNAL:
            return 2;

        case Opcode::CALL_VIRTUAL:
            return 1;

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

        case Opcode::ARG_COPY:
            return 1;

        case Opcode::DEREFERENCE:
            return 1;

        case Opcode::RETURN:
            return 0;

        case Opcode::THROW:
            return 1;

        case Opcode::INSTANTIATE:
            return 2;

        case Opcode::JUMP_CONDITIONAL:
            return 1;

        case Opcode::JUMP:
            return 1;

        case Opcode::HANDLER_DESCRIPTION:
            return 2;

        case Opcode::HANDLER_RANGE_DEFINITION:
            return 2;

        case Opcode::SENTINEL_IMPORT_TABLE_ENTRY:
            return 0;

        case Opcode::SENTINEL_IMPORT_TABLE_END:
            return 0;

        case Opcode::SENTINEL_THING_DEFINITION:
            return 2;

        case Opcode::SENTINEL_THING_EXTENDS:
            return 1;

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
