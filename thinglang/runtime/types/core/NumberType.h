/**
    NumberType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace NumberNamespace {

class NumberInstance : public BaseThingInstance {
public:
	NumberInstance() {};
	NumberInstance(int val) : val(val) {};

    virtual std::string text() override {
        return to_string(val);
    }
                

	int val;
};
typedef NumberInstance this_type;

class NumberType : public ThingTypeInternal {
public:
	NumberType() : ThingTypeInternal({&__LexicalAddition__, &__LexicalSubtraction__, &__LexicalMultiplication__, &__LexicalDivision__, &__LexicalEquality__, &__LexicalLessThan__}) {};

    Thing create(){
        return Thing(new this_type());
    }

	static Thing __LexicalAddition__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		auto __transient__1__ = self->val + other->val;
		return Thing(new this_type(__transient__1__));
		return NULL;
	}
	static Thing __LexicalSubtraction__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		auto __transient__2__ = self->val - other->val;
		return Thing(new this_type(__transient__2__));
		return NULL;
	}
	static Thing __LexicalMultiplication__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		auto __transient__3__ = self->val * other->val;
		return Thing(new this_type(__transient__3__));
		return NULL;
	}
	static Thing __LexicalDivision__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		auto __transient__4__ = self->val / other->val;
		return Thing(new this_type(__transient__4__));
		return NULL;
	}
	static Thing __LexicalEquality__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		if(self->val == other->val) {
			return Thing(new this_type(0));
		}
		return NULL;
	}
	static Thing __LexicalLessThan__() {
		auto self = Program::argument<this_type>();
		auto other = Program::argument<NumberInstance>();

		if(self->val < other->val) {
			auto __transient__5__ = self->val - other->val;
			return Thing(new this_type(__transient__5__));
		}
		return NULL;
	}
};
}