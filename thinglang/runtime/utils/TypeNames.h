#pragma once

#include <iostream>
#include <vector>
#include <stack>
#include <memory>
#include <tuple>
#include <string>
#include <fstream>
#include <sstream>
#include <set>
#include <list>
#include <forward_list>


class BaseThingInstance;
class Instruction;
class Method;
class ThingType;
class Program;

using Index = uint32_t;
using Size = Index;
using SignedIndex = int32_t;

using InstructionList = std::vector<Instruction>;
using SourceMap = std::vector<Index>;
using Source = std::vector<std::string>;

using Thing = BaseThingInstance*;
using Things = std::vector<Thing>;
using ThingForwardList = std::forward_list<Thing>;

using Frame = Things;
using FrameStack = std::forward_list<Frame>;

typedef void (*InternalMethod)();

using Methods = std::vector<Method>;
using InternalMethods = std::vector<InternalMethod>;

using Type = ThingType*;
using Types = std::vector<Type>;

using ProgramInfo = std::tuple<InstructionList, Things, Index, Size, SourceMap, Source>;

