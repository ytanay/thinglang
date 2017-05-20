#include "Program.h"
#include "../types/NoneType.h"
#include "../builtins/BuiltinOutput.h"

std::stack<PThingInstance> Program::stack;
std::vector<PThingInstance> Program::static_data;
std::vector<PThingInstance> Program::internals = {PThingInstance(new BuiltinOutput())};
std::stack<Frame> Program::frames;
PThingInstance Program::current_instance;
std::vector<TypeInfo> Program::types = { NoneType() };
