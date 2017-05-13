#pragma once

#include <vector>
#include <stack>

#include "ThingInstance.h"
#include "TypeInfo.h"


using PThingInstance = std::shared_ptr<ThingInstance>;
using Frame = std::vector<PThingInstance>;
using ProgramInfo = std::pair<std::vector<PThingInstance>, std::vector<TypeInfo>>;

class Program
{
public:

	static PThingInstance pop() {
		auto ti = stack.top();
		stack.pop();
		return ti;
	}

	static PThingInstance top() {
		return stack.top();
	}

	static void push(PThingInstance instance) {
		stack.push(instance);
	}

	static PThingInstance data(unsigned int index) {
		return static_data[index];
	}

	static void insert_data(PThingInstance data) {
		static_data.push_back(data);
	}

	static PThingInstance instance() {
		return current_instance;
	}

	static void instance(PThingInstance new_instance) {
		current_instance = new_instance;
	}

	static void create_frame(unsigned int size) {
		frames.push({});
	}

	static void pop_frame() {
		frames.pop();
	}

	static Frame& frame() {
		return frames.top();
	}

	static void load(ProgramInfo& info) {
		static_data.insert(static_data.end(), info.first.begin(), info.first.end());
		types.insert(types.end(), info.second.begin(), info.second.end());
	}

	static void start() {
		types[1].instantiate();
	}
	

private:
	Program() {}

	static std::stack<PThingInstance> stack;
	static std::vector<PThingInstance> static_data;
	static std::stack<Frame> frames;
	static std::vector<TypeInfo> types;
	static PThingInstance current_instance;
};


