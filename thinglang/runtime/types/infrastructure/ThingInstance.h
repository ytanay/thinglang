#pragma once

#include "../../utils/TypeNames.h"
#include "../../errors/RuntimeError.h"


/**
 * All thing instances derive from this empty structure
 */
class BaseThingInstance {
protected:
    BaseThingInstance() : color(0) {};

    static Things EMPTY_LIST;

public:
    virtual std::string text();

    virtual bool boolean();

    virtual Thing get(Index index);

    virtual void set(Index index, const Thing& thing);

    virtual Things children() {
        return EMPTY_LIST;
    }

    unsigned char color;


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

    std::string text() override;

    Things children() override {
        return members;
    }
};





