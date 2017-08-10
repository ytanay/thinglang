#pragma once

#include <utility>

#include "../../utils/TypeNames.h"
#include "../../containers/Method.h"


class ThingType{
public:
    explicit ThingType(Size members) : members(members) {};
    virtual Thing call(Index idx) = 0;
    virtual Thing create();;

    Size members = 0;
};

class ThingTypeExternal : public ThingType {
public:
    ThingTypeExternal(const std::string &name, Size members, Methods methods) : ThingType(members), methods(
            std::move(methods)) {};

    Thing call(Index idx) override;

    Thing create() override;;


private:

    Methods methods;
};


class ThingTypeInternal : public ThingType {
public:
    explicit ThingTypeInternal(InternalMethods methods) : ThingType(0), methods(std::move(methods)) {};

    Thing call(Index idx) override  {
        return methods[idx]();
    }



private:
    InternalMethods methods;
};