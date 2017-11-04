//
// Created by Yotam on 7/8/2017.
//

#include "ThingInstance.h"
#include "../../utils/Formatting.h"

Things BaseThingInstance::EMPTY_LIST;

std::string BaseThingInstance::text() {
    return "instance";
}

bool BaseThingInstance::boolean() {
    return true;
}

Thing BaseThingInstance::get(const Index index) {
    throw RuntimeError("Cannot get on base thing instance");
}

void BaseThingInstance::set(const Index index, const Thing &thing) {
    throw RuntimeError("Cannot set on base thing instance");
}

void ThingInstance::set(const Index index, const Thing &thing) {
    std::cerr << "Setting " << index << ": " << thing->text() << std::endl;
    members[index] = thing;
}

Thing ThingInstance::get(const Index index) {
    return members[index];
}

std::string ThingInstance::text() {
    return "instance<" + to_string(members.size()) + ">";
}
