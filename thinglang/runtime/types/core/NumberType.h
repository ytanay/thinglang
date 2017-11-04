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
 
	static Thing __constructor__();
	static Thing __addition__();
	static Thing __subtraction__();
	static Thing __multiplication__();
	static Thing __division__();
	static Thing __equals__();
	static Thing __less_than__();
    
};
