/**
    NumberType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ArgumentList.h"

namespace NumberNamespace {

class NumberInstance : public ThingInstance {
public:
	NumberInstance() {};
	NumberInstance(int val) : val(val) {};

	int val;
};
typedef NumberInstance this_type;

class NumberType : public ThingType<NumberInstance> {
public:
	NumberType() : ThingType({&__LexicalAddition__, &__LexicalSubtraction__, &__LexicalMultiplication__, &__LexicalDivision__, &__LexicalEquality__, &__LexicalLessThan__}) {};



	static Thing __LexicalAddition__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		auto __transient__0__ = self->val + other->val;
		return Thing(new this_type(__transient__0__));
		return NULL;
	}
	static Thing __LexicalSubtraction__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		auto __transient__1__ = self->val - other->val;
		return Thing(new this_type(__transient__1__));
		return NULL;
	}
	static Thing __LexicalMultiplication__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		auto __transient__2__ = self->val * other->val;
		return Thing(new this_type(__transient__2__));
		return NULL;
	}
	static Thing __LexicalDivision__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		auto __transient__3__ = self->val / other->val;
		return Thing(new this_type(__transient__3__));
		return NULL;
	}
	static Thing __LexicalEquality__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		if(self->val == other->val) {
			return Thing(new this_type(0));
		}
		return NULL;
	}
	static Thing __LexicalLessThan__(ArgumentList& args) {
		auto self = args.get<0, this_type>();
		auto other = args.get<1, this_type>();
		if(self->val < other->val) {
			auto __transient__4__ = self->val - other->val;
			return Thing(new this_type(__transient__4__));
		}
		return NULL;
	}
};
}