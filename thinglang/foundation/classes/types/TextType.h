#pragma once

#include "../../../runtime/utils/TypeNames.h"
#include "../../../runtime/types/infrastructure/ThingType.h"
#include "../../../runtime/types/infrastructure/ThingInstance.h"


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
    TextType() : ThingTypeInternal({ &__constructor__, &__addition__, &__equals__, &__not_equals__, &contains, &length, &hex, &repeat, &to_bytes, &convert_number, &from_list }) {}; // constructor
 
	static void __constructor__();
	static void __addition__();
	static void __equals__();
    static void __not_equals__();
	static void contains();
	static void length();
    static void hex();
	static void repeat();
	static void to_bytes();
	static void convert_number();
	static void from_list();
    
};
