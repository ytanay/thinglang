#include "../../../runtime/types/InternalTypes.h"

void BoolType::__constructor__() {
    throw RuntimeError("Cannot create bool instance");
}

void BoolType::__and__(){
    auto self = Program::pop();
    auto other = Program::pop();
    Program::push(self->boolean() && other->boolean());
};

void BoolType::__or__(){
    auto self = Program::pop();
    auto other = Program::pop();
    Program::push(self->boolean() || other->boolean());
};


std::string BoolInstance::text() {
    return val ? "true" : "false";
}

bool BoolInstance::boolean() {
    return val;
}

bool BoolInstance::operator==(const BaseThingInstance &other) const {
    auto other_bool = dynamic_cast<const BoolInstance*>(&other);
    return other_bool && this->val == other_bool->val;
}

size_t BoolInstance::hash() const {
    return std::hash<bool>{}(this->val);
}

