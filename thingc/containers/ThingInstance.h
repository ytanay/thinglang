#pragma once

#include <ostream>
#include <string>
#include <vector>
#include <stdexcept>

#include "../errors/RuntimeError.h"
#include "MethodDefinition.h"

class ThingInstance;

typedef void (*InternalMethod)();

class ThingInstance {
public:
	ThingInstance(std::vector<MethodDefinition> methods) : methods(methods) {};
	ThingInstance(std::vector<InternalMethod> internals) : internals(internals) {};


	virtual std::string text() const {
		throw RuntimeError("str operator not implemented");
	}

	ThingInstance operator+(const ThingInstance& other) {
        throw RuntimeError("+ operator not supported for this class");
	}

	virtual ThingInstance& copy() const {
        throw RuntimeError("copy not supported for this class");
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