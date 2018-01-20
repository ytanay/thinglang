#include "../../../runtime/types/InternalTypes.h"
#include "../../../runtime/utils/Formatting.h"


void NumberType::__constructor__() {
    Program::push(Program::create<NumberInstance>());
}


void NumberType::__addition__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();
	

	Program::push(Program::create<NumberInstance>(self->val + other->val));
}


void NumberType::__subtraction__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val - other->val));
}


void NumberType::__multiplication__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val * other->val));
}


void NumberType::__division__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

    if(other->val == 0)
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Division by zero"));

	Program::push(Program::create<NumberInstance>(self->val / other->val));
}


void NumberType::__modulus__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

    if(other->val == 0)
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Modulus by zero"));

	Program::push(Program::create<NumberInstance>(self->val % other->val));
}

void NumberType::__binary_and__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val & other->val));
}

void NumberType::__binary_or__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val | other->val));
}


void NumberType::__binary_xor__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val ^ other->val));
}


void NumberType::__equals__() {
	auto other = Program::optional<NumberInstance>();
	auto self = Program::optional<NumberInstance>();

    Program::push(other && self && self->val == other->val);
}


void NumberType::__not_equals__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

    Program::push(self->val != other->val);
}


void NumberType::__less_than__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

    Program::push(self->val < other->val);

}

void NumberType::__greater_than__() {
    auto self = Program::argument<NumberInstance>();
    auto other = Program::argument<NumberInstance>();

    Program::push(self->val > other->val);

}


std::string NumberInstance::text() {
    return to_string(val);
}

bool NumberInstance::boolean() {
    return val != 0;
}

bool NumberInstance::operator==(const BaseThingInstance &other) const {
    auto other_number = dynamic_cast<const NumberInstance*>(&other);
    return other_number && this->val == other_number->val;
}

size_t NumberInstance::hash() const {
    return std::hash<long long>{}(this->val);
}


