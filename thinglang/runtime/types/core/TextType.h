/**
    TextType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ArgumentList.h"

namespace TextNamespace {

class TextInstance : public ThingInstance {
public:
	TextInstance() {};
	TextInstance(std::string val) : val(val) {};

	std::string val;
};
typedef TextInstance this_type;

class TextType : public ThingType<TextInstance> {
public:
	TextType() : ThingType({&__LexicalAddition__, &__LexicalEquality__}) {};



	static Thing __LexicalAddition__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		auto __transient__5__ = self->val + other->val;
		return Thing(new this_type(__transient__5__));
		return NULL;
	}
	static Thing __LexicalEquality__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		if(self->val == other->val) {
			return Thing(new this_type(""));
		}
		return NULL;
	}
};
}