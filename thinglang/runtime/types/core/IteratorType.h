/**
    IteratorType.h
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




class IteratorInstance : public BaseThingInstance {
    
    public:
    explicit IteratorInstance() = default; // empty constructor
    
    explicit IteratorInstance(std::vector<Thing>::iterator current, std::vector<Thing>::iterator end) : current(current), end(end) {}; // value constructor
    
    /** Mixins **/
    
    std::string text() override;
    bool boolean() override;

    
    /** Members **/
    std::vector<Thing>::iterator current;
std::vector<Thing>::iterator end;
    
    
};


class IteratorType : public ThingTypeInternal {
    
    public:
    IteratorType() : ThingTypeInternal({ &__constructor__, &has_next, &next }) {}; // constructor
 
	static void __constructor__();
	static void has_next();
	static void next();
    
};
