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




class TextInstance : public BaseThingInstance {
    
    public:
    explicit TextInstance() = default; // empty constructor
    
    explicit TextInstance(std::string val) : val(val) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override;
    virtual bool boolean() override;

    
    /** Members **/
    std::string val;
    
    
};


class TextType : public ThingTypeInternal {
    
    public:
    TextType() : ThingTypeInternal({ &__constructor__, &__addition__, &__equals__, &contains, &length, &to_bytes, &convert_number }) {}; // constructor
 
	static void __constructor__();
	static void __addition__();
	static void __equals__();
	static void contains();
	static void length();
	static void to_bytes();
	static void convert_number();
    
};
inline std::string to_string(TextInstance* val){ return val->text(); }