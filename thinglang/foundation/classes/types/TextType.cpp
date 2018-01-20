#include <iomanip>
#include "../../../runtime/types/InternalTypes.h"
#include "../../../runtime/utils/Formatting.h"


void TextType::__constructor__() {
    Program::push(Program::create<TextInstance>());
}


void TextType::__addition__() {
	auto self = Program::pop();
	auto other = Program::pop();

	Program::push(Program::create<TextInstance>(self->text() + other->text()));
}


void TextType::__equals__() {
    auto self = Program::argument<TextInstance>();
    auto other = Program::argument<TextInstance>();

	Program::push(self && other && self->val == other->val);
}

void TextType::__not_equals__() {
    auto self = Program::argument<TextInstance>();
    auto other = Program::argument<TextInstance>();

    Program::push(self && other && self->val != other->val);
}



void TextType::contains() {
    auto self = Program::argument<TextInstance>();
	auto substring = Program::argument<TextInstance>();

	Program::push(self->val.find(substring->val) != std::string::npos);
}


void TextType::length() {
	auto self = Program::argument<TextInstance>();

	Program::push(Program::create<NumberInstance>(self->val.size()));
}


void TextType::hex() {
    auto self = Program::pop();
    static const char* const lut = "0123456789abcdef";
    auto source = self->text();
    size_t len = source.length();

    std::string output;
    output.reserve(2 * len);
    for (size_t i = 0; i < len; ++i) {
        const auto c = static_cast<const unsigned char>(source[i]);
        output.push_back(lut[c >> 4]);
        output.push_back(lut[c & 15]);
    }

    Program::push(output);
}


void TextType::to_bytes() {
	auto self = Program::pop(true);
	auto val = self->text();

	auto byte_array = Program::create<ListInstance>();
	byte_array->val.resize(val.size());

    for(auto i = 0; i < val.size(); i++)
        byte_array->val[i] = Program::create<NumberInstance>(val[i]);

    Program::push(byte_array);

}


void TextType::convert_number() {
	auto num = Program::argument<TextInstance>();

	Program::push(Program::create<NumberInstance>(to_number(num->val)));
}

void TextType::from_list() {
    auto lst = Program::argument<ListInstance>();

    std::string res;

    for(auto number : lst->val){
        res.append(1, static_cast<char>(dynamic_cast<NumberInstance*>(number)->val));
    }

    Program::push(res);

}

void TextType::repeat() {
    auto self = Program::argument<TextInstance>();
    auto count = Program::argument<NumberInstance>();

    std::ostringstream output;

    for(int i = 0; i < count->val; i++)
        output << self->val;


    Program::push(output.str());

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

