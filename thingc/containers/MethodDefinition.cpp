#include <iostream>
#include "MethodDefinition.h"
#include "../execution/Program.h"


void MethodDefinition::execute()
{
	Program::create_frame(frame_size);

    for (unsigned int i = 0; i < arguments; i++) {
        Program::frame()[i] = Program::pop();
    }

    int counter = 0;
    for (auto it = symbols.begin(); it < symbols.end();) {
		std::cerr << "[" << counter << "] ";
        auto next = it->execute();
        it += next;
        counter += next;
	};
}
