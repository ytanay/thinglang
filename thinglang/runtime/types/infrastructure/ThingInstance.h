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

};

/**
 * Thing instances deriving from thing definitions created by the user
 */
class ThingInstance : public BaseThingInstance {
    Things members;
};





