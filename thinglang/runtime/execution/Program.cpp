#include "Program.h"
#include "../types/core/TextType.h"
#include "../types/core/NumberType.h"
#include "../types/core/OutputType.h"
#include "../errors/Aborts.h"


ThingStack Program::stack;
FrameStack Program::frames;
Things Program::static_data;
Index Program::entry = 0;

Types Program::internals = {
        nullptr,
        new TextNamespace::TextType(),
        new NumberNamespace::NumberType(),
        new OutputNamespace::OutputType()
};

Types Program::types = {};


Thing Program::pop() {
    if(stack.empty())
        critical_abort(EMPTY_PROGRAM_STACK);

    auto ti = static_cast<std::shared_ptr<BaseThingInstance> &&>(stack.top());
    stack.pop();
    return ti;
}

void Program::load(ProgramInfo &info) {
    entry = std::get<0>(info);
    auto loaded_data = std::get<1>(info);
    auto loaded_types = std::get<2>(info);
    static_data.insert(static_data.end(), loaded_data.begin(), loaded_data.end());
    types.insert(types.end(), loaded_types.begin(), loaded_types.end());

}


void Program::status(Index counter, const Symbol& symbol) {
    std::cerr << "[" << counter << "] Executing symbol " << describe(symbol.opcode) << ": " << symbol.target << ", "
              << symbol.secondary << " -> [";
    std::for_each(Program::frame().begin(), Program::frame().end(),
                  [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "]" << std::endl;

}
