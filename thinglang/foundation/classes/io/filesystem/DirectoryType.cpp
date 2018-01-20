#include <dirent.h>
#include "../../../../runtime/types/InternalTypes.h"

#include <stdio.h>  /* defines FILENAME_MAX */
// #define WINDOWS  /* uncomment this line to use it for windows.*/
#ifdef WINDOWS
#include <direct.h>
#define GetCurrentDir _getcwd
#else
#include <unistd.h>
#define GetCurrentDir getcwd
#endif

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
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Cannot read file list of directory " + self->file_path));
    }

    while(auto entry = readdir(directory)) {
        contents->val.push_back(Program::intern(new DirectoryEntryInstance(std::string(entry->d_name), entry->d_type)));
    }

    Program::push(contents);
}

void DirectoryType::current_working_directory(){
    char buff[FILENAME_MAX];
    if(!GetCurrentDir(buff, FILENAME_MAX)){
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Path is too long"));
    }
    std::string current_working_dir(buff);
    Program::push(current_working_dir);
}


std::string DirectoryInstance::text() {
	return "Directory(" + this->file_path + ")";
}

bool DirectoryInstance::boolean() {
	return true;
}

