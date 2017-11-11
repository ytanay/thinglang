/**
    NumberType.h
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




class NumberInstance : public BaseThingInstance {
    
    public:
    explicit NumberInstance() = default; // empty constructor
    
    explicit NumberInstance(int val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override;
    virtual bool boolean() override;

    
    /** Members **/
    int val;
    
    
};


class NumberType : public ThingTypeInternal {
    
    public:
    NumberType() : ThingTypeInternal({ &__constructor__, &__addition__, &__subtraction__, &__multiplication__, &__division__, &__equals__, &__less_than__ }) {}; // constructor
 
	static void __constructor__();
	static void __addition__();
	static void __subtraction__();
	static void __multiplication__();
	static void __division__();
	static void __equals__();
	static void __less_than__();
    
};
