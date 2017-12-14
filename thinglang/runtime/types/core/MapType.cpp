/**
    MapType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of MapType
**/


void MapType::__constructor__() {
    Program::push(Program::create<MapInstance>());
}


void MapType::get() {
	auto key = Program::pop();
	auto self = Program::argument<MapInstance>();

	Program::push(self->container.at(key));
}

void MapType::set() {
    auto value = Program::pop();
    auto key = Program::pop();
    auto self = Program::argument<MapInstance>();

    self->container[key] = value;
}


/**
Mixins of MapType
**/

std::string MapInstance::text() {
	return to_string(container);
}

bool MapInstance::boolean() {
	return !container.empty();
}

bool MapInstance::operator==(const BaseThingInstance &other) const {
    auto other_map = dynamic_cast<const MapInstance*>(&other);
    return other_map && this->container == other_map->container;
}

size_t MapInstance::hash() const {
    throw RuntimeError("Map is a mutable object and cannot be hashed"); // TODO: throw user mode exception
}