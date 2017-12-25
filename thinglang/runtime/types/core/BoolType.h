#pragma once

#include "../../utils/TypeNames.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"


class BoolInstance : public BaseThingInstance {
    //TODO: make sure constructor cannot be called
    public:
    explicit BoolInstance() = default;
    explicit BoolInstance(bool val) : val(val) {};

    std::string text() override;
    bool boolean() override;
    size_t hash() const override;
    bool operator==(const BaseThingInstance &other) const override;


    bool val;

    ~BoolInstance() override = default;
};


class BoolType : public ThingTypeInternal {
    
    public:
    BoolType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
	static void __constructor__();
    
};
