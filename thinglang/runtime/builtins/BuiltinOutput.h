#pragma once

#include <iostream>
#include "../containers/ThingInstance.h"
#include "../types/TextInstance.h"
#include "../execution/Program.h"

class BuiltinOutput : public ThingInstance {
public:

    BuiltinOutput() : ThingInstance(BuiltinOutput::methods) {};

    static void write() {
        auto str = static_cast<TextNamespace::TextInstance *>(Program::pop().get());
        std::cout << str->text() << std::endl;
    }

    static const std::vector<InternalMethod> methods;

};
