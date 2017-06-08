/**
    TextInstance.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../execution/Program.h"
#include "../containers/ThingInstance.h"
#include "../utils/formatting.h"

namespace TextNamespace {
class TextInstance;
typedef TextInstance this_type;
class TextInstance : public ThingInstance {
public:
	TextInstance(std::string val) : val(val), ThingInstance() {}

    virtual std::string text() const override {
        return to_string(val);
    }
    
    virtual void call_method(unsigned int target) override {
        methods[target]();
    }

	static const std::vector<InternalMethod> methods;
	std::string val;
	static void __LexicalAddition__() {
		auto self = static_cast<this_type*>(Program::pop().get());
		auto other = static_cast<this_type*>(Program::pop().get());
		Program::push(PThingInstance(new this_type(self->val + other->val))); return;
	}
	static void __LexicalEquality__() {
		auto self = static_cast<this_type*>(Program::pop().get());
		auto other = static_cast<this_type*>(Program::pop().get());
		if(self->val == other->val) {
			Program::push(PThingInstance(new this_type(""))); return;
		}
		Program::push(PThingInstance(NULL)); return;
	}
};
}