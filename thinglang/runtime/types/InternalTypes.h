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
#include "core/MapType.h"
#include "core/IteratorType.h"
#include "core/ConsoleType.h"
#include "core/FileType.h"
#include "core/TimeType.h"
#include "core/ExceptionType.h"

enum class InternalTypes {
    TEXT = 1,
    NUMBER = 2,
    BOOL = 3,
    LIST = 4,
    MAP = 5,
    ITERATOR = 6,
    CONSOLE = 7,
    FILE = 8,
    TIME = 9,
    EXCEPTION = 10
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

        case InternalTypes::MAP:
            return "MAP";

        case InternalTypes::ITERATOR:
            return "ITERATOR";

        case InternalTypes::CONSOLE:
            return "CONSOLE";

        case InternalTypes::FILE:
            return "FILE";

        case InternalTypes::TIME:
            return "TIME";

        case InternalTypes::EXCEPTION:
            return "EXCEPTION";
    }
}
