#include <iostream>
#include <string>

#include "Symbol.h"
#include "Program.h"


void Symbol::execute() {
	switch (this->opcode) {

	case Opcode::NOP:
		break;

	case Opcode::PUSH: {
		Program::push(Program::frame()[this->target]);
		break;
	}

	case Opcode::PUSH_CONST: {
		Program::push(Program::data(target));
		break;
	};

	case Opcode::CALL_METHOD: {
		auto instance = Program::instance();
		auto method = instance->method(target);
		Program::create_frame(method.frame_size);

		for (unsigned int i = 0; i < method.arguments; i++) {
			Program::frame().push_back(Program::pop());
		}

		method.execute();
		break;
	}

	case Opcode::PRINT:
		std::cout << Program::pop()->text() << std::endl;
		break;

	case Opcode::CALL_INTERNAL: {
		auto instance = Program::top();
		instance->call_internal(this->target);
		break;
	}

	case Opcode::RETURN: {
		Program::pop_frame();
		break;
	}

	default: 
		throw RuntimeError("Cannot handle symbol " + std::to_string((int) this->opcode));
		break;

	}
}