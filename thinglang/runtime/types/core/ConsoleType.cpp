/**
    ConsoleType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"
#include "../../execution/Program.h"


/**
Methods of ConsoleType
**/


void ConsoleType::write() {
	auto message = Program::pop();

	std::cout << message->text();
}


void ConsoleType::print() {
	auto message = Program::pop();

	std::cout << message->text() << std::endl;
}


void ConsoleType::print_format() {
    auto params = Program::argument<ListInstance>();
    auto message = Program::pop();

    auto str = message->text();
    size_t index = 0, iterated = 0;

    while (true) {
        /* Locate the substring to replace. */
        index = str.find("{}", index);
        if (index == std::string::npos) break;

        /* Make the replacement. */
        str.replace(index, 2, params->val[iterated++]->text());

        /* Advance index forward so the next iteration doesn't pick it up as well. */
        index += 2;
    }

    std::cout << str << std::endl;
}


void ConsoleType::read_line() {
	std::string input;
	std::getline(std::cin, input);

	Program::push(Program::create<TextInstance>(input));
}

