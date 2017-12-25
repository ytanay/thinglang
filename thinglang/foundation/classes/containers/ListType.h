#pragma once


#include "../../../runtime/types/interfaces/IndexedInterface.h"
#include "../../../runtime/types/infrastructure/ThingType.h"

class ListInstance : public IndexedInterface {
    
    public:
    explicit ListInstance() = default; // empty constructor
    
    explicit ListInstance(std::vector<Thing> val) : val(std::move(val)) {}; // value constructor


	std::string text() override;
	bool boolean() override;
	size_t hash() const override;
	bool operator==(const BaseThingInstance &other) const override;

    Things val;
    
    
    Things children() override {
        return val;
    }

	~ListInstance() override = default;

};


class ListType : public ThingTypeInternal {
    
    public:
    ListType() : ThingTypeInternal({
                                           &__constructor__,
                                           &get,
                                           &set,
                                           append,
                                           &pop,
                                           &swap,
                                           &contains,
                                           &length,
                                           &iterator,
                                           &range
                                   }) {};
 
	static void __constructor__();

    static void get();
    static void set();

	static void append();
	static void pop();
    static void swap();

	static void contains();
    static void length();

	static void iterator();

	static void range();
    
};
