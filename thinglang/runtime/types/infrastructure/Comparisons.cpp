#include "Comparisons.h"
#include "ThingInstance.h"

bool ThingEquality::operator()(const Thing &t1, const Thing &t2) const {
    return (*t1) == (*t2);
}

std::size_t ThingHash::operator()(const Thing &t1) const {
    return t1->hash();
}
