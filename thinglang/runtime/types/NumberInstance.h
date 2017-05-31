#pragma once

#include "../execution/Program.h"
#include "../containers/ThingInstance.h"
#include "../utils/formatting.h"

namespace NumberNamespace {
class NumberInstance;
typedef NumberInstance this_type;
class NumberInstance : public ThingInstance {
public:
	NumberInstance(int val) : val(val), ThingInstance(this_type::methods) {}

virtual std::string text() const override {
    return to_string(val);
}
virtual void call_method(unsigned int target) override {
    internals[target]();
}

	static const std::vector<InternalMethod> methods;
	int val;
	static void __LexicalAddition__() {
		auto self = static_cast<this_type*>(Program::pop().get());
		auto other = static_cast<this_type*>(Program::pop().get());
		Program::push(PThingInstance(new this_type(self->val + other->val))); return;
	}
	static void __LexicalMultiplication__() {
		auto self = static_cast<this_type*>(Program::pop().get());
		auto other = static_cast<this_type*>(Program::pop().get());
		Program::push(PThingInstance(new this_type(self->val * other->val))); return;
	}
};
}