/**
    FileType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"


void DirectoryEntryType::__constructor__() {
    auto self = Program::create<DirectoryEntryInstance>();

    auto type = Program::argument<TextInstance>();
    auto path = Program::argument<TextInstance>();

	self->path = path;
    self->type = type;

	Program::push(self);
}


std::string DirectoryEntryInstance::text() {
	return "DirectoryEntry(" + this->path->text() + ", " + this->type->text() + ")";
}

bool DirectoryEntryInstance::boolean() {
	return true;
}

Things DirectoryEntryInstance::children() {
    return {this->path, this->type};
}

Thing DirectoryEntryInstance::get(Index index) {
    switch(index){
        case 0:
            return this->path;
        case 1:
            return this->type;
        default:
            throw RuntimeError("Cannot get " + to_string(index) + " on DirectoryEntry");
    }
}

