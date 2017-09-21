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
    LIST = 4,
    CONSOLE = 5
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

        case InternalTypes::LIST:
            return "LIST";

        case InternalTypes::CONSOLE:
            return "CONSOLE";
    }
}
