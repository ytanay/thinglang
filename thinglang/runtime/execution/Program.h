#pragma once

#include <vector>
#include <stack>
#include <cassert>
#include <algorithm>


#include "../utils/TypeNames.h"
#include "../errors/Aborts.h"
#include "../utils/Containers.h"
#include "../errors/RuntimeError.h"

class Program {

private:
    Program() = default;

    /**
     * Stack manipulation
     */

private:
    static ThingForwardList stack;
    static FrameStack frames;

public:
    static void push(const Thing& instance);
    static void push(bool instance);
    static Thing pop();
    static void create_frame(Size size);
    static void pop_frame();
    static Frame &frame();
    static void copy_args(Size count, Size offset);
    template <typename T>
    static T* argument(){
        /**
        * Pops an argument from the stack, casting it to type T*
        */
        auto value = pop();

        if(value == nullptr)
            critical_abort(AbortReason::NULL_POINTER);

        auto casted = dynamic_cast<T*>(value);

        if(casted == nullptr)
            throw RuntimeError("Cannot cast target"); // TODO: make user-mode exception

        return casted;
    }


    /**
    * Static data and infrastructure
    */

private:
    static Things static_data;
    static Index entry;
    static Size initial_frame_size;
    static SourceMap source_map;
    static Source source;
    static InstructionList instructions;
    static Types internals;

public:
    static void load(ProgramInfo &info);
    static void execute();
    static Thing data(Index index);


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

    /**
     * Diagnostics
     */
public:

    static void status(Index counter, const Instruction& instruction);

};


