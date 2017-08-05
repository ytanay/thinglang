#pragma once

#include "../../utils/TypeNames.h"

/**
 * All thing instances derive from this empty structure
 */
class BaseThingInstance {
protected:
    BaseThingInstance() {};

public:
    virtual std::string text() {
        return "?";
    }

    virtual bool boolean() {
        return true;
    }

    virtual Thing operator[](const Index index) const {
        return nullptr;
    }

};

/**
 * Thing instances deriving from thing definitions created by the user
 */
class ThingInstance : public BaseThingInstance {
    Things members;

public:
    Thing operator[](const Index index) const override {
        return members[index];
    }
};





