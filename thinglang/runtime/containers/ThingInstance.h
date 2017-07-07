#pragma once

#include <ostream>
#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>

#include "../errors/RuntimeError.h"
#include "MethodDefinition.h"



class ThingInstance {
public:
    ThingInstance(Methods methods) : methods(methods) {};
    ThingInstance(){};

    virtual bool boolean() const {
        throw RuntimeError("cannot convert to boolean");
    }


    virtual std::string text() const {
        throw RuntimeError("str operator not implemented");
    }

    ThingInstance operator+(const ThingInstance &other) {
        throw RuntimeError("+ operator not supported for this class");
    }

    virtual ThingInstance &copy() const {
        throw RuntimeError("copy not supported for this class");
    }


    virtual void call_internal(Index target) {
        throw RuntimeError("Cannot call internal method in this class");
    }

    virtual void call_method(Index target) {
        methods[target].execute();
    }

protected:
    Methods methods;
};

inline std::ostream &operator<<(std::ostream &os, const ThingInstance &instance) {
    return os << instance.text();
}