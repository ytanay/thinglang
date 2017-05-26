#include "MethodDefinition.h"
#include "../execution/Program.h"


void MethodDefinition::execute()
{
	Program::create_frame(frame_size);
	for (auto symbol : this->symbols) {
		symbol.execute();
	};
}
