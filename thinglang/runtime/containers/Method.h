#pragma once

#include <utility>
#include <vector>

#include "../execution/Instruction.h"
#include "../utils/TypeNames.h"


class Method {
public:
    Method(Size frame_size, Size arguments, Size offset, InstructionList instructions) :
            frame_size(frame_size), arguments(arguments), offset(offset), instructions(std::move(instructions)) {};

    void execute();

    // The distinction between arguments and offset is due to constructors.
    // When the constructor is called, no instance is pushed into the stack,
    // so the first argument is overwritten by the instance when it is created.
    // The offset member signifies where to start popping arguments into the stack
    Size frame_size = 0;
    Size arguments = 0;
    Size offset = 0;

private:
    InstructionList instructions;

};

