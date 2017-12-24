/**
    MapType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../utils/Containers.h"


class MapInstance : public IndexedInterface {

public:
    explicit MapInstance() = default; // empty constructor
    
    explicit MapInstance(ThingMap container) : container(std::move(container)) {}; // value constructor
    
    /** Mixins **/

    std::string text() override;
    bool boolean() override;
    size_t hash() const override;
    bool operator==(const BaseThingInstance &other) const override;

    
    /** Members **/
    ThingMap container;
    
    
    Things children() override {
        Things children(container.size() * 2);

        for(const auto& pair : container){
            children.push_back(pair.first);
            children.push_back(pair.second);
        }

        return children;
    }

    ~MapInstance() override = default;
};


class MapType : public ThingTypeInternal {
    
    public:
    MapType() : ThingTypeInternal({ &__constructor__, &get, &set, &remove, &size }) {}; // constructor

    static void __constructor__();
	static void get();
    static void set();
    static void remove();
    static void size();

};
