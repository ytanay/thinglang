#include "../../../runtime/types/InternalTypes.h"


void TimeType::__constructor__() {
    Program::push(Program::create<TimeInstance>());
}


void TimeType::now() {
    Program::push(Program::create<NumberInstance>(time(nullptr)));
}

