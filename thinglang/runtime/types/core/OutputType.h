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
	OutputInstance() {};
	OutputInstance(std::string val) : val(val) {};

    virtual std::string text() override {
        return to_string(val);
    }
                

	std::string val;
};
typedef OutputInstance this_type;

class OutputType : public ThingTypeInternal {
public:
	OutputType() : ThingTypeInternal({&write}) {};

    Thing create(){
        return Thing(new this_type());
    }

	static Thing write() {
		auto message = Program::argument<TextNamespace::TextInstance>();

		std::cout << message->text() << std::endl;
		return NULL;
	}
};
}