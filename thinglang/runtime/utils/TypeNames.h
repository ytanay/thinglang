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
#include <chrono>
#include <unordered_map>


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

typedef void (*InternalMethod)();

using Methods = std::vector<Method>;
using InternalMethods = std::vector<InternalMethod>;

using Type = ThingType*;
using TypeList = std::vector<Type>;
using TypeMap = std::unordered_map<Type, Index>;