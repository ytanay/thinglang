#pragma once

#include "TypeNames.h"
#include "../types/infrastructure/Comparisons.h"

using Things = std::vector<Thing>;
using ThingForwardList = std::forward_list<Thing>;
using ThingMap = std::unordered_map<Thing, Thing, ThingHash, ThingEquality>;

using Frame = Things;
using FrameStack = std::forward_list<Frame>;

using ProgramInfo = std::tuple<InstructionList, Things, Index, Size, SourceMap, Source>;
