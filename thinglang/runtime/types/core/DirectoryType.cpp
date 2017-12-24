/**
    FileType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include <dirent.h>
#include "../InternalTypes.h"
#include "../../execution/Program.h"

/**
Methods of Directory
**/


void DirectoryType::__constructor__() {
	auto file_path = Program::argument<TextInstance>();
	auto self = Program::create<DirectoryInstance>();

	self->file_path = file_path->text();
	Program::push(self);
}


void DirectoryType::contents() {
	auto self = Program::argument<DirectoryInstance>();

    auto contents = Program::create<ListInstance>();
    auto directory = opendir(self->file_path.c_str());

    if (directory != nullptr) { // TODO: Throw exception
        while(auto entry = readdir(directory)) {
            contents->val.push_back(Program::create<TextInstance>(entry->d_name));
        }
    }

    Program::push(contents);
}



/**
Mixins of Directory
**/

std::string DirectoryInstance::text() {
	return "Directory(" + this->file_path + ")";
}

bool DirectoryInstance::boolean() {
	return true;
}

