/**
    ListType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of ListType
**/


void ListType::__constructor__() {
    Program::push(Program::create<ListInstance>());
}


void ListType::append() {
		auto item = Program::pop();
		auto self = Program::argument<ListInstance>();

		self->val.push_back(item);
		Program::push(self);
        
    }


void ListType::pop() {
		auto self = Program::argument<ListInstance>();

		auto elem = self->val.back();
		self->val.pop_back();
		Program::push(elem);
        
    }


void ListType::contains() {
		auto item = Program::pop();
		auto self = Program::argument<ListInstance>();

		auto res = std::find(self->val.begin(), self->val.end(), item) != self->val.end();
		
        if(res) {
			Program::push(BOOL_TRUE);
        }

		
        else {
			Program::push(BOOL_FALSE);
    }

        
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

