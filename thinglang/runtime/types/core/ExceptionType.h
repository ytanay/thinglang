/**
    ExceptionType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../execution/Globals.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"




class ExceptionInstance : public BaseThingInstance {
    
    public:
    explicit ExceptionInstance() = default; // empty constructor
    
    explicit ExceptionInstance(TextInstance* message) : message(message) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override;
    virtual bool boolean() override;

    
    /** Members **/
    TextInstance* message;
    
    
};


class ExceptionType : public ThingTypeInternal {
    
    public:
    ExceptionType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
	static void __constructor__();
    
};
