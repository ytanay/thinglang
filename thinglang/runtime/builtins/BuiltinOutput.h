#pragma once

#include <iostream>
#include "../containers/ThingInstance.h"
#include "../types/TextInstance.h"
#include "../execution/Program.h"

class BuiltinOutput : public ThingInstance {
public:

    BuiltinOutput() : ThingInstance() {};

    static void write() {
        auto str = static_cast<TextNamespace::TextInstance *>(Program::pop().get());
        std::cout << str->text() << std::endl;
    }

    virtual void call_internal(unsigned int target) override {
        methods[target]();
    }

private:
    static const InternalMethods methods;

};
