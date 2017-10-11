/**
    ConsoleType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of ConsoleType
**/


Thing ConsoleType::__constructor__() {
    return Thing(new ConsoleInstance());
}


Thing ConsoleType::write() {
		auto message = Program::pop();

		std::cout << message->text();
        return nullptr;
    }


Thing ConsoleType::print() {
		auto message = Program::pop();

		std::cout << message->text() << std::endl;
        return nullptr;
    }


Thing ConsoleType::read_line() {


		std::string input;
		std::getline(std::cin, input);
		return Thing(new TextInstance(input));
        return nullptr;
    }


/**
Mixins of ConsoleInstance
**/

