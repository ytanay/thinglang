/**
    ConsoleType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of ConsoleType
**/


void ConsoleType::__constructor__() {
    Program::push(Program::create<ConsoleInstance>());
}


void ConsoleType::write() {
		auto message = Program::pop();

		std::cout << message->text();
        
    }


void ConsoleType::print() {
		auto message = Program::pop();

		std::cout << message->text() << std::endl;
        
    }


void ConsoleType::read_line() {


		std::string input;
		std::getline(std::cin, input);
		Program::push(Program::create<TextInstance>(input));
        
    }


/**
Mixins of ConsoleInstance
**/

