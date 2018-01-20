#include "../../../../runtime/types/InternalTypes.h"

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
    auto param_size = params->val.size();
    size_t index = 0, iterated = 0;


    while(true){
        index = str.find("{}", index);
        if(index == std::string::npos) break;
        if(iterated >= param_size) throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Not enough format arguments provided"));

        auto contents = params->val[iterated++]->text();
        str.replace(index, 2, contents);

        index += contents.size();
    }

    std::cout << str << std::endl;
}

void ConsoleType::read_line() {
	std::string input;
	std::getline(std::cin, input);

	Program::push(Program::create<TextInstance>(input));
}

