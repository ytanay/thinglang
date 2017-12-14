#pragma once

#include "../../utils/TypeNames.h"

class ThingEquality  {
public:
    bool operator() (const Thing& t1, const Thing& t2) const;
};

class ThingHash {
public:
    std::size_t operator() (const Thing& t1) const;
};