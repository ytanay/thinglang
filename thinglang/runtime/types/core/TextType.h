/**
    TextType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace TextNamespace {

class TextInstance : public BaseThingInstance {
public:
	TextInstance() {};
	TextInstance(std::string val) : val(val) {};

    virtual std::string text() override {
        return to_string(val);
    }
                

	std::string val;
};
typedef TextInstance this_type;

class TextType : public ThingTypeInternal {
public:
	TextType() : ThingTypeInternal({&__LexicalAddition__, &__LexicalEquality__}) {};

    Thing create(){
        return Thing(new this_type());
    }

	static Thing __LexicalAddition__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<TextNamespace::TextInstance>();

		auto __transient__5__ = self->val + other->val;
		return Thing(new this_type(__transient__5__));
		return NULL;
	}
	static Thing __LexicalEquality__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<TextNamespace::TextInstance>();

		if(self->val == other->val) {
			return Thing(new this_type(""));
		}
		return NULL;
	}
};
}