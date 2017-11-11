#include "ThingType.h"


void ThingTypeInternal::call(Index idx) {
    methods[idx]();
}
