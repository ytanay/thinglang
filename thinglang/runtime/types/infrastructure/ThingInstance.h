#pragma once

#include "../../utils/TypeNames.h"
#include "../../errors/RuntimeError.h"
#include "../../utils/Containers.h"


/**
 * All thing instances derive from this empty structure
 */
class BaseThingInstance {
protected:
    BaseThingInstance() : color(0) {};

    static Things EMPTY_LIST;

public:

    virtual Thing get(Index index);
    virtual void set(Index index, const Thing& thing);
    virtual std::string text();
    virtual bool boolean();
    virtual size_t hash() const;
    virtual bool operator==(const BaseThingInstance &other) const;
    virtual Type type() const;

    virtual Things children() {
        return EMPTY_LIST;
    }

    unsigned char color;

    virtual ~BaseThingInstance() = default;


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





