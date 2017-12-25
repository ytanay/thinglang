#include "IteratorType.h"
#include "../../../runtime/execution/Program.h"

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


std::string IteratorInstance::text() {
    return "Iterator<ListType>";
}

bool IteratorInstance::boolean() {
    return current != end;
}

