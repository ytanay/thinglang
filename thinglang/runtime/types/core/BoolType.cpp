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
    Program::push(Program::create<BoolInstance>()); // TODO: is this necessary?
}


/**
Mixins of BoolInstance
**/

std::string BoolInstance::text() {
    return val ? "true" : "false";
}

bool BoolInstance::boolean() {
    return val;
}

