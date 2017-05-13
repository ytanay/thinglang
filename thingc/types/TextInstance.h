#pragma once

#include <string>

#include "../containers/ThingInstance.h"

class TextInstance : public ThingInstance {

public:
	TextInstance(const std::string& str) : str(str), ThingInstance(TextInstance::methods) {};

	virtual std::string text() const override {
		return str;
	}


private:
	std::string str;
	static const std::vector<InternalMethod> methods;
};

