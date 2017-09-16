#include "ThingType.h"


Thing ThingTypeExternal::call(Index idx) {
    methods[idx].execute();
    return nullptr;
}

