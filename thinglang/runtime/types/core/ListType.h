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

namespace ListNamespace {


class ListInstance : public BaseThingInstance {
    
    public:
    explicit ListInstance() = default; // empty constructor
    explicit ListInstance(std::vector<Thing> val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override {
        return to_string(val);
    }
    
    bool boolean() override {
        return to_boolean(val);
    }
    
    /** Members **/
    
    std::vector<Thing> val;
};


typedef ListInstance this_type;

class ListType : public ThingTypeInternal {
    
    public:
    ListType() : ThingTypeInternal({ &__constructor__, &append }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }


    static Thing append() {
		auto item = Program::pop();
		auto self = Program::argument<this_type>();

		self->val.push_back(item);
		return nullptr;
    }

    
};

}