/**
    ConsoleType.h
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

namespace ConsoleNamespace {


class ConsoleInstance : public BaseThingInstance {
    
    public:
    explicit ConsoleInstance() = default; // empty constructor
    
    
    
    /** Mixins **/
    
    
    
    /** Members **/
    
    
};


typedef ConsoleInstance this_type;

class ConsoleType : public ThingTypeInternal {
    
    public:
    ConsoleType() : ThingTypeInternal({ &__constructor__, &write, &print, &read_line }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }


    static Thing write() {
		auto message = Program::pop();

		std::cout << message->text();
		return nullptr;
    }


    static Thing print() {
		auto message = Program::pop();

		std::cout << message->text() << std::endl;
		return nullptr;
    }


    static Thing read_line() {


		std::string input;
		std::getline(std::cin, input);
		return Thing(new TextNamespace::TextInstance(input));
		return nullptr;
    }

    
};

}