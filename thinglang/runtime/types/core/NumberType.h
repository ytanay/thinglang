/**
    NumberType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../execution/Globals.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace NumberNamespace {


class NumberInstance : public BaseThingInstance {
    
    public:
    explicit NumberInstance() = default; // empty constructor
    
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
    NumberType() : ThingTypeInternal({ &__constructor__, &__addition__, &__subtraction__, &__multiplication__, &__division__, &__equals__, &__less_than__ }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }


    static Thing __addition__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val + other->val));
		return nullptr;
    }


    static Thing __subtraction__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val - other->val));
		return nullptr;
    }


    static Thing __multiplication__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val * other->val));
		return nullptr;
    }


    static Thing __division__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val / other->val));
		return nullptr;
    }


    static Thing __equals__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		
        if(self->val == other->val) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

		return nullptr;
    }


    static Thing __less_than__() {
		auto other = Program::argument<NumberNamespace::NumberInstance>();
		auto self = Program::argument<this_type>();

		
        if(self->val < other->val) {
			return BOOL_TRUE;
        }

		return nullptr;
    }

    
};

}