#pragma once

#include <ostream>
#include <string>
#include <vector>

#include "MethodDefinition.h"

class ThingInstance;

typedef void (*InternalMethod)();

class ThingInstance {
public:
	ThingInstance(std::vector<MethodDefinition> methods) : methods(methods) {};
	ThingInstance(std::vector<InternalMethod> internals) : internals(internals) {};


	virtual std::string text() const {
		return "str operator not implemented";
		throw std::exception("str operator not implemented");
	}

	ThingInstance operator+(const ThingInstance& other) {
		throw std::exception("+ operator not supported for this class");
	}

	virtual ThingInstance& copy() const {
		throw std::exception("copy not supported for this class");
	}
	
	virtual void call(unsigned int target) {
		
		methods[target].execute();
	}

	virtual void call_internal (unsigned int target) {
		internals[target]();
	}

	MethodDefinition method(unsigned int target) const {
		return methods[target];
	}

private:
	std::vector<ThingInstance> fields;
	std::vector<MethodDefinition> methods;
	std::vector<InternalMethod> internals;
};

inline std::ostream &operator<<(std::ostream &os, const ThingInstance &instance) {
	return os << instance.text();
}