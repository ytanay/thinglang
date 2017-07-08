#pragma once

#include "../../utils/TypeNames.h"
#include "../../containers/MethodDefinition.h"


class ThingType{
public:
    virtual Thing call(Index idx) = 0;
    virtual Thing create() {
        return NULL;
    };
};

class ThingTypeExternal : public ThingType {
public:
    ThingTypeExternal(std::string name, std::string b, Methods methods) : methods(methods) {};

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
    ThingTypeInternal(LocalMethods methods) : methods(methods) {};

    Thing call(Index idx) override  {
        return methods[idx]();
    }


private:
    LocalMethods methods;
};