/**
    ListType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of ListType
**/


void ListType::__constructor__() {
    Program::push(Program::create<ListInstance>());
}


void ListType::append() {
	auto item = Program::pop();
	auto self = Program::argument<ListInstance>();

	self->val.push_back(item);
	Program::push(self);
}


void ListType::pop() {
	auto self = Program::argument<ListInstance>();

	auto elem = self->val.back();
	self->val.pop_back();
	Program::push(elem);
}


void ListType::contains() {
	auto item = Program::pop();
	auto self = Program::argument<ListInstance>();

	Program::push(std::find(self->val.begin(), self->val.end(), item) != self->val.end());
}


void ListType::iterator() {
	auto self = Program::argument<ListInstance>();

	Program::push(Program::create<IteratorInstance>(*self));
}


void ListType::get() {
	auto index = Program::argument<NumberInstance>();
	auto self = Program::argument<ListInstance>();

	Program::push(self->val[index->val]);
}


void ListType::length() {
	auto self = Program::argument<ListInstance>();

	Program::push(Program::create<NumberInstance>(self->val.size()));
}


void ListType::swap() {
	auto index2 = Program::argument<NumberInstance>();
	auto index1 = Program::argument<NumberInstance>();
	auto self = Program::argument<ListInstance>();

	auto i = index1->val, j = index2->val;
	auto temp = self->val[i];
	self->val[i] = self->val[j];
	self->val[j] = temp;
}


void ListType::range() {
	auto end = Program::argument<NumberInstance>();
	auto start = Program::argument<NumberInstance>();

	auto lst = Program::create<ListInstance>();
	lst->val.resize(static_cast<unsigned int>(end->val - start->val));
	for(auto idx = start->val, val = 0; idx < end->val; idx++, val++) lst->val[idx] = Program::create<NumberInstance>(val);
	Program::push(lst);
}


/**
Mixins of ListInstance
**/

std::string ListInstance::text() {
	return to_string(val);
}

bool ListInstance::boolean() {
	return val.size() != 0;
}

