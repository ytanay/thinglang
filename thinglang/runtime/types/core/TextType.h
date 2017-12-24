/**
    TextType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"


class TextInstance : public BaseThingInstance {

public:
    explicit TextInstance() = default; // empty constructor
    
    explicit TextInstance(std::string val) : val(std::move(val)) {}; // value constructor
    
    /** Mixins **/
    
    std::string text() override;
    bool boolean() override;
    size_t hash() const override;
    bool operator==(const BaseThingInstance &other) const override;



    /** Members **/
    std::string val;

	~TextInstance() override = default;

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
