#include "ThingType.h"


Thing ThingTypeInternal::call(Index idx) {
    return methods[idx]();
}
