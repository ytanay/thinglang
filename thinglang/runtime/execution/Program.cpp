#include "Program.h"
#include "../types/core/TextType.h"
#include "../types/core/NumberType.h"
#include "../types/core/ListType.h"
#include "../types/core/ConsoleType.h"
#include "../errors/Aborts.h"


ThingStack Program::stack;
FrameStack Program::frames;
Things Program::static_data;
Index Program::entry = 0;
SourceMap Program::source_map;
Source Program::source;

Types Program::internals = {
        nullptr,
        new TextType(),
        new NumberType(),
        new BoolType(),
        new ListType(),
        new ConsoleType()
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
    auto loaded_types = static_cast<std::vector<Type> &&>(std::get<0>(info));
    auto loaded_data = static_cast<std::vector<Thing> &&>(std::get<1>(info));
    auto loaded_source_map = static_cast<SourceMap &&>(std::get<3>(info));
    auto loaded_source = static_cast<Source &&>(std::get<4>(info));

    entry = std::get<2>(info);

    static_data.insert(static_data.end(), loaded_data.begin(), loaded_data.end());
    types.insert(types.end(), loaded_types.begin(), loaded_types.end());
    source_map.insert(source_map.end(), loaded_source_map.begin(), loaded_source_map.end());
    source.insert(source.end(), loaded_source.begin(), loaded_source.end());
}


void Program::status(Index counter, const Instruction& instruction) {
    auto source_idx = source_map[instruction.index];

    assert(source_idx < source.size());

    std::cerr << "[" << counter << "] Executing instruction " << describe(instruction.opcode) << ": " << instruction.target << ", "
              << instruction.secondary << " -> [";
    std::for_each(Program::frame().begin(), Program::frame().end(),
                  [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "] -> [" << trim(source[source_idx]) << "]" << std::endl;

}
