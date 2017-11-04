/**
    ListType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of ListType
**/


Thing ListType::__constructor__() {
    return Program::create<ListInstance>();
}


Thing ListType::append() {
		auto item = Program::pop();
		auto self = Program::argument<ListInstance>();

		self->val.push_back(item);
		return self;
        return nullptr;
    }


Thing ListType::contains() {
		auto item = Program::pop();
		auto self = Program::argument<ListInstance>();

		auto res = std::find(self->val.begin(), self->val.end(), item) != self->val.end();
		
        if(res) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

        return nullptr;
    }


/**
Mixins of ListInstance
**/

std::string ListInstance::text() {
    return to_string(val);
}

bool ListInstance::boolean() {
    return to_boolean(val);
}

