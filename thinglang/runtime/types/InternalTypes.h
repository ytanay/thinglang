/**
    InternalTypes.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include <string>

enum class InternalTypes {
    NONE = 0,
    TEXT = -1,
    NUMBER = -2
};

inline std::string describe(InternalTypes val){
     switch (val){
        
    case InternalTypes::NONE:
        return "NONE";

    case InternalTypes::TEXT:
        return "TEXT";

    case InternalTypes::NUMBER:
        return "NUMBER";
    }

}