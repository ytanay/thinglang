#pragma once

#include <string>

#include "../execution/Program.h"
#include "../containers/ThingInstance.h"


class NumberInstance : public ThingInstance {
public:

	NumberInstance(int val) : val(val), ThingInstance(NumberInstance::methods) {};

	virtual std::string text() const override {
		return std::to_string(val);
	}

	static void add() {
		auto lhs = static_cast<NumberInstance*>(Program::pop().get());
		auto rhs = static_cast<NumberInstance*>(Program::pop().get());
		auto ptr = PThingInstance(new NumberInstance(lhs->val + rhs->val));
		Program::push(ptr);
	}

	const int val;
	static const std::vector<InternalMethod> methods;
	
};

