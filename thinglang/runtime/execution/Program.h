#pragma once

#include <vector>
#include <stack>
#include <cassert>
#include <algorithm>


#include "../utils/TypeNames.h"


class Program {
public:



    template <typename T>
    static T* argument(){
        return static_cast<T*>(pop());
    };

    static Thing pop();

    static void push(const Thing& instance) {
        stack.push_front(instance);
    }

    static Thing data(Index index) {
        return static_data[index];
    }

    static void create_frame(Size size) {
        frames.push_front(Frame(size));
    }

    static void pop_frame() {
        frames.pop_front();
    }

    static Frame &frame() {
        return frames.front();
    }

    static void execute();
    static void copy_args(Size count, Size offset);

    static void load(ProgramInfo &info);

    static void status(Index counter, const Instruction& instruction);

    static Types internals;

private:
    Program() = default;

    static ThingForwardList stack;
    static FrameStack frames;
    static Things static_data;
    static Index entry;
    static Size initial_frame_size;
    static SourceMap source_map;
    static Source source;
    static InstructionList instructions;



};


