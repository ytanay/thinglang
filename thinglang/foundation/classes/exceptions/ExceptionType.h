#pragma once

#include "../../../runtime/utils/TypeNames.h"
#include "../types/TextType.h"


class ExceptionInstance : public BaseThingInstance {
    
    public:
    explicit ExceptionInstance() = default; // empty constructor
    
    explicit ExceptionInstance(TextInstance* message) : message(message) {}; // value constructor

    
    std::string text() override;
    bool boolean() override;

	Type type() const override;

    Things children() override;

    TextInstance* message{};

    ~ExceptionInstance() override = default;
};


class ExceptionType : public ThingTypeInternal {
    
    public:
    ExceptionType() : ThingTypeInternal({ &__constructor__ }) {}; // constructor
 
	static void __constructor__();
    
};
