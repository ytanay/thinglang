#include "MethodDefinition.h"
#include "../execution/Program.h"


void MethodDefinition::execute()
{
	Program::create_frame(frame_size);

    for (unsigned int i = 0; i < arguments; i++) {
        Program::frame()[i] = Program::pop();
    }

    for (auto symbol : this->symbols) {
		symbol.execute();
	};
}
