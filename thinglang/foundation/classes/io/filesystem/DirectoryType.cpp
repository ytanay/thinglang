#include <dirent.h>
#include "../../../../runtime/types/InternalTypes.h"


void DirectoryType::__constructor__() {
    auto self = Program::create<DirectoryInstance>();
	auto file_path = Program::argument<TextInstance>();

	self->file_path = file_path->text();
	Program::push(self);
}


void DirectoryType::contents() {
	auto self = Program::argument<DirectoryInstance>();

    auto contents = Program::create<ListInstance>();
    auto directory = opendir(self->file_path.c_str());

    if (directory == nullptr) {
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Cannot read directory contents"));
    }

    while(auto entry = readdir(directory)) {
        contents->val.push_back(Program::intern(new DirectoryEntryInstance(std::string(entry->d_name), entry->d_type)));
    }

    Program::push(contents);
}


std::string DirectoryInstance::text() {
	return "Directory(" + this->file_path + ")";
}

bool DirectoryInstance::boolean() {
	return true;
}

