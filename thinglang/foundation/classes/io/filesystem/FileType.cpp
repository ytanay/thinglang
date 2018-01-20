#include "../../../../runtime/types/InternalTypes.h"

#include <sys/types.h>
#include <sys/stat.h>
#ifndef WIN32
#include <unistd.h>
#endif

#ifdef WIN32
#define stat _stat
#endif

void FileType::__constructor__() {
	auto self = Program::create<FileInstance>();
	auto file_path = Program::argument<TextInstance>();

	self->file_path = file_path->text();
	Program::push(self);
}

void FileType::__construct_and_open__(){
    auto self = Program::create<FileInstance>();
    auto mode = Program::argument<TextInstance>();
    auto file_path = Program::argument<TextInstance>();

    self->file_path = file_path->text();
    self->open(mode->text());
    Program::push(self);
}


void FileType::open() {
    auto self = Program::argument<FileInstance>();
	auto mode = Program::argument<TextInstance>();
    self->open(mode->text());
}


void FileType::close() {
	auto self = Program::argument<FileInstance>();

	self->file.close();
}


void FileType::write() {
    auto self = Program::argument<FileInstance>();
	auto contents = Program::argument<TextInstance>();
    if(!self->file.is_open())
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Open the file before writing"));


    self->file << contents->text();
}


void FileType::read() {
	auto self = Program::argument<FileInstance>();
    if(!self->file.is_open())
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Open the file before reading"));

	std::stringstream sstr;
	sstr << self->file.rdbuf();
	Program::push(Program::create<TextInstance>(sstr.str()));
}


void FileType::modify_time(){
    auto self = Program::argument<FileInstance>();
    struct stat result;
    if(stat(self->file_path.c_str(), &result) != 0)
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Cannot check modified times for " + self->file_path));

    auto mod_time = result.st_mtime;
    Program::push(static_cast<int64_t>(mod_time));
}

std::string FileInstance::text() {
	return "File(" + this->file_path + ")";
}

bool FileInstance::boolean() {
	return file.good();
}


void FileInstance::open(std::string mode) {
    if(file.is_open()){
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("File is already open"));
    }

    if(mode == "r") {
        file.open(file_path, std::ios::in);
    } else if(mode == "w") {
        file.open(file_path, std::ios::out);
    } else if(mode == "rb") {
        file.open(file_path, std::ios::in | std::ios::binary);
    } else if(mode == "wb"){
        file.open(file_path, std::ios::out | std::ios::binary);
    } else {
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Invalid file mode (" + mode + ")"));
    }

    if(!file.is_open()){
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Could not open file at (" + file_path + ")"));
    }
}
