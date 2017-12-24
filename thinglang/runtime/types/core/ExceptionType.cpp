/**
    ExceptionType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"
#include "../../execution/Program.h"

/**
Methods of ExceptionType
**/


void ExceptionType::__constructor__() {
    auto message = Program::argument<TextInstance>();
    auto self = Program::create<ExceptionInstance>();

    self->message = message;
}


/**
Mixins of ExceptionInstance
**/

std::string ExceptionInstance::text() {
    return message->text();
}

bool ExceptionInstance::boolean() {
    return true;
}

