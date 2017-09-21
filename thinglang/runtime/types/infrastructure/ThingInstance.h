#pragma once

#include "../../utils/TypeNames.h"
#include "../../errors/RuntimeError.h"

/**
 * All thing instances derive from this empty structure
 */
class BaseThingInstance {
protected:
    BaseThingInstance() = default;

public:
    virtual std::string text();

    virtual bool boolean();

    virtual Thing get(Index index);

    virtual void set(Index index, const Thing& thing);

};

/**
 * Thing instances deriving from thing definitions created by the user
 */
class ThingInstance : public BaseThingInstance {
    Things members;

public:

    explicit ThingInstance(Size members) : members(members) {};

    Thing get(Index index) override;

    void set(Index index, const Thing& thing) override;
};





