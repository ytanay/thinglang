#pragma once

#include <vector>
#include <stack>
#include <memory>

class BaseThingInstance;
class Symbol;
class MethodDefinition;
class ThingType;
class Program;

using Index = uint32_t;
using Size = Index;
using SignedIndex = int32_t;

using SymbolList = std::vector<Symbol>;

using Thing = std::shared_ptr<BaseThingInstance>;
using Things = std::vector<Thing>;
using ThingStack = std::stack<Thing>;

using Frame = Things;
using FrameStack = std::stack<Frame>;

typedef Thing (*InternalMethod)();

using Methods = std::vector<MethodDefinition>;
using InternalMethods = std::vector<InternalMethod>;

using Type = ThingType*;
using Types = std::vector<Type>;

