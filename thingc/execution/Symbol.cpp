#include <iostream>

#include "Symbol.h"
#include "Program.h"


int Symbol::execute() {
    std::cerr << "Executing symbol " << describe(this->opcode) << ": " << this->target << ", " << this->secondary << std::endl;

    switch (this->opcode) {

	case Opcode::NOP:
		break;

	case Opcode::PUSH: {
        Program::push(Program::frame()[this->target]);
        break;
    };

	case Opcode ::PUSH_NULL: {
		Program::push(NULL);
		break;
	}

	case Opcode::POP: {
		Program::pop();
		break;
	}

    case Opcode::SET_STATIC: {
        Program::frame()[this->target] = Program::data(secondary);
    	break;
	}

	case Opcode::SET: {
		Program::frame()[this->target] = Program::pop();
		break;
	}

	case Opcode::PUSH_STATIC: {
		Program::push(Program::data(target));
		break;
	};

	case Opcode::CALL_METHOD: {
		auto instance = Program::instance();
		auto method = instance->method(target);

		method.execute();
		break;
	}

	case Opcode::PRINT:
		std::cout << Program::pop()->text() << std::endl;
		break;

	case Opcode::CALL_INTERNAL: {
		Program::internals[this->target]->call_internal(this->secondary);
		break;
	}

	case Opcode::RETURN: {
		Program::pop_frame();
		break;
	}

    case Opcode::JUMP: {
        return target;
    }

	case Opcode::CONDITIONAL_JUMP: {
		auto value = Program::pop();
		if(!value->boolean()){
			return target;
		}
		break;
	}

	default: 
		throw RuntimeError("Cannot handle symbol " + describe(opcode) + " (" + std::to_string((int) this->opcode) + ")");
	}

	return 1;
}