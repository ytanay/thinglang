#include "../InternalTypes.h"
#include "../../execution/Program.h"
#include "../../utils/Formatting.h"


void NumberType::__constructor__() {
    Program::push(Program::create<NumberInstance>());
}


void NumberType::__addition__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val + other->val));
}


void NumberType::__subtraction__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val - other->val));
}


void NumberType::__multiplication__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val * other->val));
}


void NumberType::__division__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val / other->val));
}


void NumberType::__modulus__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val % other->val));
}

void NumberType::__binary_and__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val & other->val));
}

void NumberType::__binary_or__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val | other->val));
}


void NumberType::__binary_xor__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<NumberInstance>(self->val ^ other->val));
}


void NumberType::__equals__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

    Program::push(self->val == other->val);
}


void NumberType::__not_equals__() {
	auto other = Program::argument<NumberInstance>();
	auto self = Program::argument<NumberInstance>();

    Program::push(self->val != other->val);
}


void NumberType::__less_than__() {
    auto other = Program::argument<NumberInstance>();
    auto self = Program::argument<NumberInstance>();

    Program::push(self->val < other->val);

}

void NumberType::__greater_than__() {
    auto other = Program::argument<NumberInstance>();
    auto self = Program::argument<NumberInstance>();

    Program::push(self->val > other->val);

}

void NumberType::convert_text() {
	auto self = Program::argument<NumberInstance>();

	Program::push(Program::create<TextInstance>(to_string(self->val)));
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
    return std::hash<int>{}(this->val);
}


