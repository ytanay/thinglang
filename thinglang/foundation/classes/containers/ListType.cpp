#include "../../../runtime/types/InternalTypes.h"
#include "../../../runtime/utils/Formatting.h"

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


void ListType::set() {
    auto value = Program::pop();
    auto index = Program::argument<NumberInstance>();
    auto self = Program::argument<ListInstance>();

    self->val[index->val] = value;
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
	for(long long idx = start->val, val = 0; idx < end->val; idx++, val++) lst->val[idx] = Program::create<NumberInstance>(val);
	Program::push(lst);
}


std::string ListInstance::text() {
	return to_string(val);
}

bool ListInstance::boolean() {
	return !val.empty();
}

bool ListInstance::operator==(const BaseThingInstance &other) const {
    auto other_list = dynamic_cast<const ListInstance*>(&other);
    return other_list && this->val == other_list->val;
}

size_t ListInstance::hash() const {
    throw RuntimeError("List is a mutable object and cannot be hashed"); // TODO: throw user mode exception
}

