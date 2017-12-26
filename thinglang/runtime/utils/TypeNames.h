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
class ThingTypeInternal;
class ThingTypeUser;
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

using InternalType = ThingTypeInternal*;
using InternalTypeList = std::vector<InternalType>;
using InternalTypeMap = std::unordered_map<InternalType, Index>;

using UserType = ThingTypeUser;
using UserTypeList = std::vector<UserType>;
