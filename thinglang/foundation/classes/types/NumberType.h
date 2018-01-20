#pragma once

#include "../../../runtime/utils/TypeNames.h"


class NumberInstance : public BaseThingInstance {
    
    public:
    explicit NumberInstance() = default; // empty constructor
    
    explicit NumberInstance(int val) : val(val) {}; // value constructor
    
    /** Mixins **/

	std::string text() override;
	bool boolean() override;
	size_t hash() const override;
	bool operator==(const BaseThingInstance &other) const override;

    
    /** Members **/
    long long val{};
    
    
	~NumberInstance() override = default;
};


class NumberType : public ThingTypeInternal {
    
    public:
    NumberType() : ThingTypeInternal({
											 &__constructor__,

											 &__addition__,
											 &__subtraction__,
											 &__multiplication__,
											 &__division__,
											 &__modulus__,

                                             &__binary_and__,
                                             &__binary_or__,
                                             &__binary_xor__,

											 &__equals__,
											 &__not_equals__,
											 &__less_than__,
											 &__greater_than__,
                                             &__sqrt__
											  }) {};
 
	static void __constructor__();
	static void __addition__();
	static void __subtraction__();
	static void __multiplication__();
	static void __division__();
	static void __modulus__();
	static void __binary_and__();
	static void __binary_or__();
	static void __binary_xor__();
	static void __equals__();
	static void __not_equals__();
	static void __less_than__();
	static void __greater_than__();
	static void __sqrt__();
    
};
