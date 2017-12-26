#pragma once

#include "TypeNames.h"
#include "../types/infrastructure/Comparisons.h"

using Things = std::vector<Thing>;
using ThingForwardList = std::forward_list<Thing>;
using ThingMap = std::unordered_map<Thing, Thing, ThingHash, ThingEquality>;

using Frame = Things;
using FrameStack = std::forward_list<Frame>;


struct ProgramInfo {
    InstructionList instructions;
    Things static_data;
    UserTypeList user_types;
    InternalTypeList imported_types;
    Index entry_point;
    Size root_stack_frame_size;
    SourceMap source_map;
    Source program_source;
};

template <class T>
T* singleton()
{
    static T x;
    return &x;
}