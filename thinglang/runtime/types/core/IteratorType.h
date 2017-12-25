#pragma once

#include "../../utils/TypeNames.h"
#include "ListType.h"


class IteratorInstance : public BaseThingInstance {
    
    public:

    explicit IteratorInstance(ListInstance& base) : base(base), current(base.val.begin()), end(base.val.end()) {}; // value constructor

    std::string text() override;
    bool boolean() override;

    ListInstance& base;
    Things::const_iterator current;
    Things::const_iterator end;

	Things children() override {
        return {dynamic_cast<Thing>(&base)};
	}

    ~IteratorInstance() override = default;
    
    
};


class IteratorType : public ThingTypeInternal {
    
    public:
    IteratorType() : ThingTypeInternal({ &__constructor__, &has_next, &next }) {}; // constructor
 
	static void __constructor__();
	static void has_next();
	static void next();
    
};
