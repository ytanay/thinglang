/**
    TimeType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of TimeType
**/


void TimeType::__constructor__() {
    Program::push(Program::create<TimeInstance>());
}


void TimeType::now() {
    Program::push(Program::create<NumberInstance>(std::chrono::system_clock::now().time_since_epoch().count()));
}

