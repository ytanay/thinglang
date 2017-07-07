#pragma once

#include <vector>
#include <stack>

#include "../utils/TypeNames.h"
#include "../containers/ThingInstance.h"
#include "../types/TypeInfo.h"


using ProgramInfo = std::pair<std::vector<Thing>, std::vector<TypeInfo>>;

class Program {
public:

    static Thing pop() {
        auto ti = stack.top();
        stack.pop();
        return ti;
    }

    static Thing top() {
        return stack.top();
    }

    static void push(Thing instance) {
        stack.push(instance);
    }

    static Thing data(Index index) {
        return static_data[index];
    }

    static Thing instance() {
        return current_instance;
    }

    static void instance(Thing new_instance) {
        current_instance = new_instance;
    }

    static void create_frame(Size size) {
        frames.push(Frame(size));
    }

    static void pop_frame() {
        frames.pop();
    }

    static Frame &frame() {
        return frames.top();
    }

    static void load(ProgramInfo &info) {
        static_data.insert(static_data.end(), info.first.begin(), info.first.end());
        types.insert(types.end(), info.second.begin(), info.second.end());
    }

    static void start() {
        types[1].instantiate();
    }

    static Things internals;
    static Things static_data;

private:
    Program() {}

    static ThingStack stack;


    static FrameStack frames;
    static std::vector<TypeInfo> types;
    static Thing current_instance;
};


