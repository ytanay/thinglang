/**
    NumberType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of NumberType
**/


void NumberType::__constructor__() {
    Program::push(Program::create<NumberInstance>());
}


void NumberType::__addition__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		Program::push(Program::create<NumberInstance>(self->val + other->val));
        
    }


void NumberType::__subtraction__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		Program::push(Program::create<NumberInstance>(self->val - other->val));
        
    }


void NumberType::__multiplication__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		Program::push(Program::create<NumberInstance>(self->val * other->val));
        
    }


void NumberType::__division__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		Program::push(Program::create<NumberInstance>(self->val / other->val));
        
    }


void NumberType::__equals__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		
        if(self->val == other->val) {
			Program::push(BOOL_TRUE);
        }

		
        else {
			Program::push(BOOL_FALSE);
    }

        
    }


void NumberType::__less_than__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		
        if(self->val < other->val) {
			Program::push(BOOL_TRUE);
        }

		
        else {
			Program::push(BOOL_FALSE);
    }

        
    }


/**
Mixins of NumberInstance
**/

std::string NumberInstance::text() {
    return to_string(val);
}

bool NumberInstance::boolean() {
    return to_boolean(val);
}

