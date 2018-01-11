#include "../../../../runtime/types/InternalTypes.h"

void FileType::__constructor__() {
	auto self = Program::create<FileInstance>();
	auto file_path = Program::argument<TextInstance>();

	self->file_path = file_path->text();
	Program::push(self);
}


void FileType::open() {
    auto self = Program::argument<FileInstance>();
	auto mode = Program::argument<TextInstance>();
    auto mode_type = mode->text();

	if(mode_type == "r") {
		self->file.open(self->file_path, std::ios::in);
	} else if(mode_type == "w") {
		self->file.open(self->file_path, std::ios::out);
	} else if(mode_type == "rb") {
        self->file.open(self->file_path, std::ios::in | std::ios::binary);
    } else if(mode_type == "wb"){
        self->file.open(self->file_path, std::ios::out | std::ios::binary);
    } else {
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Invalid file mode (" + mode_type + ")"));
    }

    if(!self->file.is_open()){
        throw Program::create<ExceptionInstance>(Program::create<TextInstance>("Could not open file at (" + self->file_path + ")"));
    }

}


void FileType::close() {
	auto self = Program::argument<FileInstance>();

	self->file.close();
}


void FileType::write() {
    auto self = Program::argument<FileInstance>();
	auto contents = Program::argument<TextInstance>();

	self->file << contents->text();
}


void FileType::read() {
	auto self = Program::argument<FileInstance>();

	std::stringstream sstr;
	sstr << self->file.rdbuf();
	Program::push(Program::create<TextInstance>(sstr.str()));
}


std::string FileInstance::text() {
	return "File(" + this->file_path + ")";
}

bool FileInstance::boolean() {
	return file.good();
}

