#pragma once

#include <vector>
#include <stack>
#include <memory>

class ThingInstance;
class Symbol;
class MethodDefinition;

typedef void (*InternalMethod)();

using Index = size_t;
using Size = size_t;

using SymbolList = std::vector<Symbol>;

using Thing = std::shared_ptr<ThingInstance>;
using Things = std::vector<Thing>;

using ThingStack = std::stack<Thing>;

using Frame = Things;
using FrameStack = std::stack<Frame>;

using Methods = std::vector<MethodDefinition>;
using InternalMethods = std::vector<InternalMethod>;