/**
    TextType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of TextType
**/


Thing TextType::__constructor__() {
    return Thing(new TextInstance());
}


Thing TextType::__addition__() {
		auto other = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		return Thing(new TextInstance(self->val + other->val));
        return nullptr;
    }


Thing TextType::__equals__() {
		auto other = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		
        if(self->val == other->val) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

        return nullptr;
    }


Thing TextType::contains() {
		auto substring = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		auto found = self->val.find(substring->val) != std::string::npos;
		
        if(found) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

        return nullptr;
    }


Thing TextType::convert_number() {
		auto num = Program::argument<TextInstance>();

		return Thing(new NumberInstance(to_number(num->val)));
        return nullptr;
    }


/**
Mixins of TextInstance
**/

std::string TextInstance::text() {
    return to_string(val);
}

bool TextInstance::boolean() {
    return to_boolean(val);
}

