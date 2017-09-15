/**
    TextType.h
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

namespace TextNamespace {


class TextInstance : public BaseThingInstance {
    
    public:
    explicit TextInstance(std::string val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override {
        return to_string(val);
    }
    
    bool boolean() override {
        return to_boolean(val);
    }
    
    /** Members **/
    
    std::string val;
};


typedef TextInstance this_type;

class TextType : public ThingTypeInternal {
    
    public:
    TextType() : ThingTypeInternal({ &__addition__, &__equals__, &contains }) {}; // constructor
    
    
    static Thing __addition__() {
		auto other = Program::argument<TextNamespace::TextInstance>();
		auto self = Program::argument<this_type>();

		return Thing(new this_type(self->val + other->val));
		return nullptr;
    }


    static Thing __equals__() {
		auto other = Program::argument<TextNamespace::TextInstance>();
		auto self = Program::argument<this_type>();

		
        if(self->val == other->val) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

		return nullptr;
    }


    static Thing contains() {
		auto substring = Program::argument<TextNamespace::TextInstance>();
		auto self = Program::argument<this_type>();

		auto found = self->val.find(substring->val) != std::string::npos;
		
        if(found) {
			return BOOL_TRUE;
        }

		
        else {
			return BOOL_FALSE;
    }

		return nullptr;
    }

    
};

}