#pragma once

#include "../../../runtime/utils/TypeNames.h"

class ObjectType : public ThingTypeInternal {
    
    public:
    ObjectType() : ThingTypeInternal({
                                             nullptr,

											 &__equals__,
                                             &as_text
                                     }) {};
 
	static void __equals__();
	static void as_text();
    
};
