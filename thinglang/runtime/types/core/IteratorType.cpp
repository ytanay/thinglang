/**
    IteratorType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"
#include "../../execution/Program.h"
#include "../../execution/Globals.h"

/**
Methods of IteratorType
**/


void IteratorType::__constructor__() {
    throw RuntimeError("Cannot instantiate Iterator directly");
}


void IteratorType::has_next() {
	auto self = Program::argument<IteratorInstance>();

	Program::push(self->current != self->end);
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
    return "Iterator<ListType>";
}

bool IteratorInstance::boolean() {
    return current != end;
}

