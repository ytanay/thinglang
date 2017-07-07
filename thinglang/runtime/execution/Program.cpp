#include "Program.h"
#include "../types/NoneType.h"
#include "../builtins/BuiltinOutput.h"

ThingStack Program::stack;
Things Program::static_data;
Things Program::internals = {Thing(new BuiltinOutput())};
FrameStack Program::frames;
Thing Program::current_instance;
std::vector<TypeInfo> Program::types = {NoneType()};
