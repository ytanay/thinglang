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
    virtual bool boolean() override {
        return to_boolean(val);
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
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val + other->val));
		return NULL;
	}
	static Thing __LexicalSubtraction__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val - other->val));
		return NULL;
	}
	static Thing __LexicalMultiplication__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val * other->val));
		return NULL;
	}
	static Thing __LexicalDivision__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val / other->val));
		return NULL;
	}
	static Thing __LexicalEquality__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		if(self->val == other->val) {
			return Thing(new this_type(1));
		}
		else {
			return Thing(new this_type(0));
		}
		return NULL;
	}
	static Thing __LexicalLessThan__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		if(self->val < other->val) {
			return Thing(new this_type(self->val - other->val));
		}
		return NULL;
	}
};
}