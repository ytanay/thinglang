/**
    NumberType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of NumberType
**/


Thing NumberType::__constructor__() {
    return Thing(new NumberInstance());
}


Thing NumberType::__addition__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		return Thing(new NumberInstance(self->val + other->val));
        return nullptr;
    }


Thing NumberType::__subtraction__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		return Thing(new NumberInstance(self->val - other->val));
        return nullptr;
    }


Thing NumberType::__multiplication__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		return Thing(new NumberInstance(self->val * other->val));
        return nullptr;
    }


Thing NumberType::__division__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		return Thing(new NumberInstance(self->val / other->val));
        return nullptr;
    }


Thing NumberType::__equals__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		
        if(self->val == other->val) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

        return nullptr;
    }


Thing NumberType::__less_than__() {
		auto other = Program::argument<NumberInstance>();
		auto self = Program::argument<NumberInstance>();

		
        if(self->val < other->val) {
			return BOOL_TRUE;
        }

        return nullptr;
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

