#pragma once

#include <ostream>
#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>

#include "../errors/RuntimeError.h"
#include "MethodDefinition.h"

class ThingInstance;

typedef void (*InternalMethod)();

class ThingInstance {
public:
	ThingInstance(std::vector<MethodDefinition> methods) : methods(methods) {};
	ThingInstance(std::vector<InternalMethod> internals) : internals(internals) {std::cerr << "Created with " << internals.size() << std::endl;};

	virtual bool boolean() const {
		throw RuntimeError("cannot convert to boolean");
	}


	virtual std::string text() const {
		throw RuntimeError("str operator not implemented");
	}

	ThingInstance operator+(const ThingInstance& other) {
        throw RuntimeError("+ operator not supported for this class");
	}

	virtual ThingInstance& copy() const {
        throw RuntimeError("copy not supported for this class");
	}


	virtual void call_internal (unsigned int target) {
		internals[target]();
	}

	virtual void call_method(unsigned int target) {
		methods[target].execute();
	}

protected:
	std::vector<ThingInstance> fields;
	std::vector<MethodDefinition> methods;
	std::vector<InternalMethod> internals;
};

inline std::ostream &operator<<(std::ostream &os, const ThingInstance &instance) {
	return os << instance.text();
}