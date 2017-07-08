#include "Program.h"
#include "../types/core/TextType.h"
#include "../types/core/NumberType.h"
#include "../builtins/Output.h"
#include <iostream>

ThingStack Program::stack;
FrameStack Program::frames;
Things Program::static_data;

Types Program::internals = {NULL, new TextNamespace::TextType(), new NumberNamespace::NumberType(), new OutputNamespace::OutputType()};
Types Program::types = {};

Thing Program::current_instance;


ThingType* Program::type(SignedIndex index) {
    return types[index];
}

Thing Program::pop() {
    if(stack.empty())  // TODO: remove check
        throw RuntimeError("Empty program stack");

    auto ti = stack.top();
    stack.pop();
    return ti;
}

void Program::load(ProgramInfo &info) {
    static_data.insert(static_data.end(), info.first.begin(), info.first.end());
    types.insert(types.end(), info.second.begin(), info.second.end());
}


void Program::status(Index counter, const Symbol& symbol) {
    std::cerr << "[" << counter << "] Executing symbol " << describe(symbol.opcode) << ": " << symbol.target << ", "
              << symbol.secondary << " -> [";
    std::for_each(Program::frame().begin(), Program::frame().end(),
                  [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "] -> [";
    std::for_each(Program::static_data.begin(), Program::static_data.end(),
                  [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "]" << std::endl;

}
