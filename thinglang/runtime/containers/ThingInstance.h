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
    ThingInstance(){};

    virtual void call(Index target) = 0;

    virtual std::string text() const {
        throw RuntimeError("conversion to text not implemented");
    }


};

inline std::ostream &operator<<(std::ostream &os, const ThingInstance &instance) {
    return os << instance.text();
}