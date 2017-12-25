#pragma once

#include "../../../runtime/utils/TypeNames.h"


class TimeInstance : public BaseThingInstance {
    
    public:
    explicit TimeInstance() = default; // empty constructor

	~TimeInstance() override = default;
};


class TimeType : public ThingTypeInternal {
    
    public:
    TimeType() : ThingTypeInternal({ &__constructor__, &now }) {}; // constructor
 
	static void __constructor__();
	static void now();
    
};
