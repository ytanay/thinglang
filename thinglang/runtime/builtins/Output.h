/**
    OutputType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../utils/TypeNames.h"
#include "../types/infrastructure/ThingType.h"
#include "../types/infrastructure/ThingInstance.h"
#include "../execution/Program.h"
#include <iostream>

namespace OutputNamespace {

class OutputInstance : public BaseThingInstance {
public:
	OutputInstance() {};
	OutputInstance(int val) : val(val) {};

	int val;
};
typedef OutputInstance this_type;

class OutputType : public ThingTypeInternal {
public:
	OutputType() : ThingTypeInternal({&write}) {};

    Thing create(){
        return Thing(new this_type());
    }

	static Thing write() {
		std::cout << Program::pop()->text() << std::endl;
		return NULL;
	}

};
}