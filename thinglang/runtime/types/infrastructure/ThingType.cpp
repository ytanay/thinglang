#include "ThingType.h"

Thing ThingTypeExternal::call(Index idx) {
    methods[idx].execute();
    return nullptr;
}

Thing ThingTypeExternal::create() {
    methods[0].execute();
    return nullptr;
}

Thing ThingType::create() {
    return nullptr;
}
