#include "Program.h"
#include "../types/NoneType.h"

std::stack<PThingInstance> Program::stack;
std::vector<PThingInstance> Program::static_data;
std::stack<Frame> Program::frames;
PThingInstance Program::current_instance;
std::vector<TypeInfo> Program::types = { NoneType() };
