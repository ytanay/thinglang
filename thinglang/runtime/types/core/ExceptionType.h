/**
    ExceptionType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "TextType.h"


class ExceptionInstance : public BaseThingInstance {
    
    public:
    explicit ExceptionInstance() = default; // empty constructor
    
    explicit ExceptionInstance(TextInstance* message) : message(message) {}; // value constructor
    
    /** Mixins **/
    
    std::string text() override;
    bool boolean() override;

    
    /** Members **/
    TextInstance* message{};

    ~ExceptionInstance() override = default;
};


class ExceptionType : public ThingTypeInternal {
    
    public:
    ExceptionType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
	static void __constructor__();
    
};
