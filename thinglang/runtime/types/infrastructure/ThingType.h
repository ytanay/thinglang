#pragma once

#include "../../utils/TypeNames.h"
#include "../../containers/Method.h"


class ThingType{
public:
    ThingType(Size members) : members(members) {};
    virtual Thing call(Index idx) = 0;
    virtual Thing create() {
        return NULL;
    };

    Size members = 0;
};

class ThingTypeExternal : public ThingType {
public:
    ThingTypeExternal(std::string name, Size members, Methods methods) : ThingType(members), methods(methods) {};

    Thing call(Index idx) override  {
        methods[idx].execute();
        return NULL;
    }

    virtual Thing create() override {
        methods[0].execute();
        return NULL;
    };


private:

    Methods methods;
};


class ThingTypeInternal : public ThingType {
public:
    ThingTypeInternal(InternalMethods methods) : ThingType(0), methods(methods) {};

    Thing call(Index idx) override  {
        return methods[idx]();
    }



private:
    InternalMethods methods;
};