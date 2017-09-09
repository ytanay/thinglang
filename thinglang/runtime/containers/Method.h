#pragma once

#include <utility>
#include <vector>

#include "../execution/Instruction.h"
#include "../utils/TypeNames.h"


class Method {
public:
    Method(Size frame_size, Size arguments, InstructionList symbols) :
            frame_size(frame_size), arguments(arguments), symbols(std::move(symbols)) {};

    void execute();

    Size frame_size = 0;
    Size arguments = 0;

private:
    InstructionList symbols;

};

