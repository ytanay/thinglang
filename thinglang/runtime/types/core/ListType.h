/**
    ListType.h
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




class ListInstance : public BaseThingInstance {
    
    public:
    explicit ListInstance() = default; // empty constructor
    
    explicit ListInstance(std::vector<Thing> val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override;
    virtual bool boolean() override;

    
    /** Members **/
    std::vector<Thing> val;
    
    
    Things& children() override {
        return val;
    }

};


class ListType : public ThingTypeInternal {
    
    public:
    ListType() : ThingTypeInternal({ &__constructor__, &append, &pop, &contains }) {}; // constructor
 
	static Thing __constructor__();
	static Thing append();
	static Thing pop();
	static Thing contains();
    
};
