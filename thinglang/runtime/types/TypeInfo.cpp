#include "TypeInfo.h"
#include "../execution/Program.h"


void TypeInfo::instantiate() {
    Program::instance(Thing(new ThingInstance(this->methods)));
    this->methods[0].execute();

}
