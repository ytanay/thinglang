/**
    IteratorType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of IteratorType
**/


void IteratorType::__constructor__() {
    Program::push(Program::create<IteratorInstance>());
}


void IteratorType::has_next() {
		auto self = Program::argument<IteratorInstance>();

		Program::push(Program::create<BoolInstance>(self->current != self->end));
        
    }


void IteratorType::next() {
		auto self = Program::argument<IteratorInstance>();

		auto item = *self->current++;
		Program::push(item);
        
    }


/**
Mixins of IteratorInstance
**/

std::string IteratorInstance::text() {
    return to_string(current);
}

bool IteratorInstance::boolean() {
    return to_boolean(current);
}

