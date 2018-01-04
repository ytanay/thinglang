#include "MapType.h"
#include "../../../runtime/execution/Program.h"
#include "../../../runtime/utils/Formatting.h"

void MapType::__constructor__() {
    Program::push(Program::create<MapInstance>());
}


void MapType::get() {
    auto self = Program::argument<MapInstance>();
    auto key = Program::pop();

	Program::push(self->container.at(key));
}

void MapType::set() {
    auto self = Program::argument<MapInstance>();
    auto value = Program::pop();
    auto key = Program::pop();

    self->container[key] = value;
}

void MapType::remove() {
    auto self = Program::argument<MapInstance>();
    auto key = Program::pop();

    auto value = self->container.at(key);

    self->container.erase(key);

    Program::push(value);
}

void MapType::size() {
    auto self = Program::argument<MapInstance>();

    Program::push(static_cast<int64_t>(self->container.size()));
}

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
