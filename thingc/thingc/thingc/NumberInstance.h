#pragma once

#include <string>

#include "Program.h"
#include "ThingInstance.h"


class NumberInstance : public ThingInstance {
public:

	NumberInstance(int val) : val(val), ThingInstance(NumberInstance::methods) {};

	virtual std::string text() const override {
		return std::to_string(val);
	}


	const int val;
	static const std::vector<InternalMethod> methods;
	
};

