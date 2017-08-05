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

    virtual Thing get(const Index index) {
        throw RuntimeError("Cannot get on base thing instance");
    }

    virtual void set(const Index index, const Thing& thing) {
        throw RuntimeError("Cannot set on base thing instance");
    }

};

/**
 * Thing instances deriving from thing definitions created by the user
 */
class ThingInstance : public BaseThingInstance {
    Things members;

public:

    ThingInstance(Size members) : members(members), BaseThingInstance() {};


    virtual Thing get(const Index index) override {
        return members[index];
    }

    virtual void set(const Index index, const Thing& thing) override {
        std::cerr << "Setting " << index << ": " << thing->text() << std::endl;
        members[index] = thing;
    }
};





