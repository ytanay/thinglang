#pragma once

#include <utility>

#include "../../utils/TypeNames.h"


class ThingType{
public:
    explicit ThingType(Size members) : members(members) {};
    virtual Thing call(Index idx) = 0;

    Size members = 0;
};


class ThingTypeInternal : public ThingType {
public:
    explicit ThingTypeInternal(InternalMethods methods) : ThingType(0), methods(std::move(methods)) {};

    Thing call(Index idx) override;

private:
    InternalMethods methods;
};