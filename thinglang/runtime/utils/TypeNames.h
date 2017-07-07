#pragma once

#include <vector>
#include <stack>
#include <memory>

class ThingInstance;
class Symbol;

using Index = size_t;

using SymbolList = std::vector<Symbol>;

using Thing = std::shared_ptr<ThingInstance>;
using Things = std::vector<Thing>;

using ThingStack = std::stack<Thing>;

using Frame = Things;
using FrameStack = std::stack<Frame>;
