#include "TypeInfo.h"
#include "Program.h"


void TypeInfo::instantiate()
{
	Program::instance(PThingInstance(new ThingInstance(this->methods)));
	this->methods[0].execute();

}
