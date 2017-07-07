#pragma once

#include <vector>

#include "../execution/Symbol.h"
#include "../utils/TypeNames.h"


class MethodDefinition {
public:
    MethodDefinition() : frame_size(0), arguments(0) {};

    MethodDefinition(Size frame_size, Size arguments, SymbolList symbols) :
            frame_size(frame_size), arguments(arguments), symbols(symbols) {};

    void execute();

    Size frame_size;
    Size arguments;

private:
    SymbolList symbols;

};

