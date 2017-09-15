/**
    InternalTypes.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class InternalTypes {
    NONE = 0,
    TEXT = 1,
    NUMBER = 2,
    BOOL = 3,
    OUTPUT = 4
};


inline auto describe(InternalTypes val){
    switch (val){
        
        case InternalTypes::NONE:
            return "NONE";

        case InternalTypes::TEXT:
            return "TEXT";

        case InternalTypes::NUMBER:
            return "NUMBER";

        case InternalTypes::BOOL:
            return "BOOL";

        case InternalTypes::OUTPUT:
            return "OUTPUT";
    }
}
