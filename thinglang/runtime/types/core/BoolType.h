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




class BoolInstance : public BaseThingInstance {
    
    public:
    explicit BoolInstance() = default; // empty constructor
    
    explicit BoolInstance(bool val) : val(val) {}; // value constructor
    
    /** Mixins **/

    std::string text() override;
    bool boolean() override;
    size_t hash() const override;
    bool operator==(const BaseThingInstance &other) const override;

    
    /** Members **/
    bool val;
    
    
    ~BoolInstance() override = default;
};


class BoolType : public ThingTypeInternal {
    
    public:
    BoolType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
	static void __constructor__();
    
};
