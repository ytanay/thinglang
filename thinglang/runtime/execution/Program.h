#pragma once

#include <vector>
#include <stack>
#include <cassert>
#include <algorithm>

#include "../utils/TypeNames.h"
#include "../containers/ThingInstance.h"
#include "../types/TypeInfo.h"


using ProgramInfo = std::pair<std::vector<Thing>, std::vector<TypeInfo>>;

class Program {
public:

    static TypeInfo type(SignedIndex index);

    static Thing pop();

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

    static void start() {
        types[1].instantiate();
    }

    static void load(ProgramInfo &info);

    static void status(Index counter, const Symbol& symbol);


private:
    Program() {}

    static ThingStack stack;
    static FrameStack frames;
    static Things static_data;

    static Types internals;
    static Types types;

    static Thing current_instance;

};


