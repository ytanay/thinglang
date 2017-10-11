/**
    InternalTypes.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#pragma once

#include <string>

#include "core/TextType.h"
#include "core/NumberType.h"
#include "core/BoolType.h"
#include "core/ListType.h"
#include "core/ConsoleType.h"
#include "core/FileType.h"

enum class InternalTypes {
    TEXT = 1,
    NUMBER = 2,
    BOOL = 3,
    LIST = 4,
    CONSOLE = 5,
    FILE = 6
};


inline auto describe(InternalTypes val){
    switch (val){
        
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

        case InternalTypes::FILE:
            return "FILE";
    }
}
