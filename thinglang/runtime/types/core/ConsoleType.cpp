#include "../InternalTypes.h"

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
        index = str.find("{}", index);
        if (index == std::string::npos) break;

        str.replace(index, 2, params->val[iterated++]->text());

        index += 2;
    }

    std::cout << str << std::endl;
}

void ConsoleType::read_line() {
	std::string input;
	std::getline(std::cin, input);

	Program::push(Program::create<TextInstance>(input));
}

