#include "../../../runtime/types/InternalTypes.h"


void ObjectType::__equals__() {
	auto other = Program::optional<BaseThingInstance>();
	auto self = Program::optional<BaseThingInstance>();

    Program::push(self == other);
}


void ObjectType::as_text() {
	auto self = Program::pop();
	Program::push(self->text());
}



