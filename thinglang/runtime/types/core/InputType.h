/**
    InputType.h
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

namespace InputNamespace {


class InputInstance : public BaseThingInstance {
    
    public:
    explicit InputInstance() = default; // empty constructor
    
    
    
    /** Mixins **/
    
    
    
    /** Members **/
    
    
};


typedef InputInstance this_type;

class InputType : public ThingTypeInternal {
    
    public:
    InputType() : ThingTypeInternal({ &__constructor__, &read_line }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }


    static Thing read_line() {


		std::string input;
		std::getline(std::cin, input);
		return Thing(new TextNamespace::TextInstance(input));
		return nullptr;
    }

    
};

}