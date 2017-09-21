/**
    BoolType.h
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

namespace BoolNamespace {


class BoolInstance : public BaseThingInstance {
    
    public:
    explicit BoolInstance() = default; // empty constructor
    
    explicit BoolInstance(bool val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    
    virtual std::string text() override {
        return to_string(val);
    }
    
    bool boolean() override {
        return to_boolean(val);
    }

    
    /** Members **/
    
    bool val;
};


typedef BoolInstance this_type;

class BoolType : public ThingTypeInternal {
    
    public:
    BoolType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }

    
};

}