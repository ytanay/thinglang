/**
    OutputType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace OutputNamespace {


class OutputInstance : public BaseThingInstance {
    
    public:
    explicit OutputInstance(std::string val) : val(val) {}; // value constructor
    
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


typedef OutputInstance this_type;

class OutputType : public ThingTypeInternal {
    
    public:
    OutputType() : ThingTypeInternal({ &write }) {}; // constructor
    
    
    static Thing write() {
		auto message = Program::argument<TextNamespace::TextInstance>();

		std::cout << message->text() << std::endl;
		return nullptr;
    }

    
};

}