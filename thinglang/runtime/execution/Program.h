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



    /**
     * Allocation and garbage collection components
     */

private:
    static ThingForwardList objects; // All allocated thing instances
    static unsigned char current_mark; // The value used to mark objects in the current cycle

public:

    template <typename T, typename... Args>
    static T* create(Args&&... args) {
        // Create a new ThingInstance and intern into a generation
        auto thing = new T(std::forward<Args>(args)...);
        objects.push_front(thing);
        return thing;

    }

    template <typename T, typename... Args>
    static T* permanent(Args&&... args) {
        // Create a new ThingInstance into perm-gen
        auto thing = new T(std::forward<Args>(args)...);
        return thing;
    }

    static void gc_cycle(); // Full mark-sweep cycle
    static void mark(); // Recursively descends into all roots
    static void mark(const Thing& thing); //  Marks an instance and recursively descends into its references
    static void sweep(); // Collects all marked instances
    static auto object_count() { // WARNING: costs O(n)
        return std::distance(objects.begin(), objects.end());
    }


};


