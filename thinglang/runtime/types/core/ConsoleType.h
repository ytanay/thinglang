/**
    ConsoleType.h
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




class ConsoleInstance : public BaseThingInstance {
    
    public:
    explicit ConsoleInstance() = default; // empty constructor
    
    
    
    /** Mixins **/
    
    
    /** Members **/
    
    
    
};


class ConsoleType : public ThingTypeInternal {
    
    public:
    ConsoleType() : ThingTypeInternal({ &__constructor__, &write, &print, &read_line }) {}; // constructor
 
	static void __constructor__();
	static void write();
	static void print();
	static void read_line();
    
};
