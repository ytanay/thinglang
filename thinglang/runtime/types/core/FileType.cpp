/**
    FileType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of FileType
**/


void FileType::__constructor__() {
	auto file_path = Program::argument<TextInstance>();
	auto self = Program::create<FileInstance>();

	self->file_path = file_path->text();
	Program::push(self);
}


void FileType::open() {
	auto mode = Program::argument<TextInstance>();
	auto self = Program::argument<FileInstance>();

	if(mode->text() == "r") {
		self->file.open(self->file_path, std::ios::in);
	} else if(mode->text() == "w") {
		self->file.open(self->file_path, std::ios::out);
	} else {
		throw RuntimeError("Invalid file mode"); // TODO: throw user exception
	}
}


void FileType::close() {
	auto self = Program::argument<FileInstance>();

	self->file.close();
}


void FileType::write() {
	auto contents = Program::argument<TextInstance>();
	auto self = Program::argument<FileInstance>();

	self->file << contents->text();
}


void FileType::read() {
	auto self = Program::argument<FileInstance>();

	std::stringstream sstr;
	sstr << self->file.rdbuf();
	Program::push(Program::create<TextInstance>(sstr.str()));
}


/**
Mixins of FileInstance
**/

std::string FileInstance::text() {
	return "File(" + this->file_path + ")";
}

bool FileInstance::boolean() {
	return file.good();
}

