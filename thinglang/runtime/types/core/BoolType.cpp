/**
    BoolType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of BoolType
**/


void BoolType::__constructor__() {
    Program::push(Program::create<BoolInstance>());
}


/**
Mixins of BoolInstance
**/

std::string BoolInstance::text() {
    return to_string(val);
}

bool BoolInstance::boolean() {
    return to_boolean(val);
}

