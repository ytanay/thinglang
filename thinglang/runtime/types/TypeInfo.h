#pragma once

#include <string>

#include "../utils/TypeNames.h"
#include "../containers/MethodDefinition.h"
#include "../containers/ThingInstance.h"

class TypeInfo {

public:
    TypeInfo(const std::string &name) : name(name) {};

    TypeInfo(const std::string &name, std::string members, std::vector<MethodDefinition> &methods) : name(name),
                                                                                                     members(members),
                                                                                                     methods(methods) {};

    void instantiate();

private:
    std::string name;
    std::string members;
    std::vector<MethodDefinition> methods;
};

