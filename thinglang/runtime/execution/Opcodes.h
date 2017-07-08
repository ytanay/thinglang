/**
    Opcode.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include <string>

enum class Opcode {
    INVALID = 0,
    NOP = 1,
    PUSH = 2,
    PUSH_STATIC = 3,
    PUSH_NULL = 4,
    POP = 5,
    SET = 6,
    SET_STATIC = 7,
    CALL = 8,
    CALL_INTERNAL = 9,
    RETURN = 10,
    JUMP = 11,
    CONDITIONAL_JUMP = 12,
    PRINT = 13,
    METHOD_END = 14
};

inline std::string describe(Opcode val){
     switch (val){
        
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

    case Opcode::CALL_INTERNAL:
        return "CALL_INTERNAL";

    case Opcode::RETURN:
        return "RETURN";

    case Opcode::JUMP:
        return "JUMP";

    case Opcode::CONDITIONAL_JUMP:
        return "CONDITIONAL_JUMP";

    case Opcode::PRINT:
        return "PRINT";

    case Opcode::METHOD_END:
        return "METHOD_END";
    }

}