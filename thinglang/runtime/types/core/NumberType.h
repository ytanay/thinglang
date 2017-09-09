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
    explicit NumberInstance(int val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override {
        return to_string(val);
    }
    
    bool boolean() override {
        return to_boolean(val);
    }
    
    /** Members **/
    
    int val;
};


typedef NumberInstance this_type;

class NumberType : public ThingTypeInternal {
    
    public:
    NumberType() : ThingTypeInternal({ &__LexicalAddition__, &__LexicalSubtraction__, &__LexicalMultiplication__, &__LexicalDivision__, &__LexicalEquality__, &__LexicalLessThan__ }) {}; // constructor
    
    
    static Thing __LexicalAddition__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val + other->val));
		return nullptr;
    }


    static Thing __LexicalSubtraction__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val - other->val));
		return nullptr;
    }


    static Thing __LexicalMultiplication__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val * other->val));
		return nullptr;
    }


    static Thing __LexicalDivision__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val / other->val));
		return nullptr;
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

		return nullptr;
    }


    static Thing __LexicalLessThan__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		
        if(self->val < other->val) {
			return Thing(new this_type(self->val - other->val));
        }

		return nullptr;
    }

    
};

}