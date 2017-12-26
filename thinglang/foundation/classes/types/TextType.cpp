#include "../../../runtime/types/InternalTypes.h"
#include "../../../runtime/execution/Program.h"
#include "../../../runtime/utils/Formatting.h"


void TextType::__constructor__() {
    Program::push(Program::create<TextInstance>());
}


void TextType::__addition__() {
	auto self = Program::argument<TextInstance>();
	auto other = Program::pop();

	Program::push(Program::create<TextInstance>(self->val + other->text()));
}


void TextType::__equals__() {
    auto self = Program::argument<TextInstance>();
    auto other = Program::argument<TextInstance>();

	Program::push(self && other && self->val == other->val);
}


void TextType::contains() {
    auto self = Program::argument<TextInstance>();
	auto substring = Program::argument<TextInstance>();

	Program::push( self->val.find(substring->val) != std::string::npos);
}


void TextType::length() {
	auto self = Program::argument<TextInstance>();

	Program::push(Program::create<NumberInstance>(self->val.size()));
}


void TextType::to_bytes() {
	auto self = Program::argument<TextInstance>();

	auto byte_array = Program::create<ListInstance>();
	byte_array->val.resize(self->val.size());
	for(auto i = 0; i < self->val.size(); i++) byte_array->val[i] = Program::create<NumberInstance>(self->val[i]);
	Program::push(byte_array);

}


void TextType::convert_number() {
	auto num = Program::argument<TextInstance>();

	Program::push(Program::create<NumberInstance>(to_number(num->val)));
}


std::string TextInstance::text() {
    return val;
}

bool TextInstance::boolean() {
    return !val.empty();
}

bool TextInstance::operator==(const BaseThingInstance &other) const {
    auto other_text = dynamic_cast<const TextInstance*>(&other);
    return other_text && this->val == other_text->val;
}

size_t TextInstance::hash() const {
    return std::hash<std::string>{}(this->val);
}

