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
#include "core/TimeType.h"
#include "core/ExceptionType.h"
#include "core/IteratorType.h"

enum class InternalTypes {
    TEXT = 1,
    NUMBER = 2,
    BOOL = 3,
    LIST = 4,
    CONSOLE = 5,
    FILE = 6,
    TIME = 7,
    EXCEPTION = 8,
    ITERATOR = 9
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

        case InternalTypes::TIME:
            return "TIME";

        case InternalTypes::EXCEPTION:
            return "EXCEPTION";

        case InternalTypes::ITERATOR:
            return "ITERATOR";
    }
}
