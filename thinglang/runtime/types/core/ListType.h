/**
    ListType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include <utility>

#include "../../utils/TypeNames.h"
#include "../interfaces/IndexedInterface.h"


class ListInstance : public IndexedInterface {
    
    public:
    explicit ListInstance() = default; // empty constructor
    
    explicit ListInstance(std::vector<Thing> val) : val(std::move(val)) {}; // value constructor
    
    /** Mixins **/

	std::string text() override;
	bool boolean() override;
	size_t hash() const override;
	bool operator==(const BaseThingInstance &other) const override;

    
    /** Members **/
    Things val;
    
    
    Things children() override {
        return val;
    }

};


class ListType : public ThingTypeInternal {
    
    public:
    ListType() : ThingTypeInternal({ &__constructor__, &append, &pop, &contains, &iterator, &get, &length, &swap, &range }) {}; // constructor
 
	static void __constructor__();
	static void append();
	static void pop();
	static void contains();
	static void iterator();
	static void get();
	static void length();
	static void swap();
	static void range();
    
};
