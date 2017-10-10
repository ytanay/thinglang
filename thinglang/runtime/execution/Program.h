#pragma once

#include <vector>
#include <stack>
#include <cassert>
#include <algorithm>


#include "../utils/TypeNames.h"


class Program {
public:

    template <typename T>
    static std::shared_ptr<T> argument(){
        return std::static_pointer_cast<T>(pop());
    };

    static Thing pop();

    static void push(const Thing& instance) {
        stack.push(instance);
    }

    static Thing data(Index index) {
        return static_data[index];
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

    static void execute();
    static void copy_args(Size count, Size offset);

    static void load(ProgramInfo &info);

    static void status(Index counter, const Instruction& instruction);

    static Types internals;

private:
    Program() = default;

    static ThingStack stack;
    static FrameStack frames;
    static Things static_data;
    static Index entry;
    static Size initial_frame_size;
    static SourceMap source_map;
    static Source source;
    static InstructionList instructions;



};


