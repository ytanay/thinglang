/**
    FileType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of FileType
**/


Thing FileType::__constructor__() {
		auto file_path = Program::argument<TextInstance>();
		auto self = Program::create<FileInstance>();

		self->file_path = file_path->text();
        return self;
    }


Thing FileType::open() {
		auto mode = Program::argument<TextInstance>();
		auto self = Program::argument<FileInstance>();

		
        if(mode->text() == "r") {
			self->file.open(self->file_path, std::ios::in);
        }

		
        else if(mode->text() == "w") {
			self->file.open(self->file_path, std::ios::out);
        }

        return nullptr;
    }


Thing FileType::close() {
		auto self = Program::argument<FileInstance>();

		self->file.close();
        return nullptr;
    }


Thing FileType::write() {
		auto contents = Program::argument<TextInstance>();
		auto self = Program::argument<FileInstance>();

		self->file << contents->text();
        return nullptr;
    }


Thing FileType::read() {
		auto self = Program::argument<FileInstance>();

		std::stringstream sstr;
		sstr << self->file.rdbuf();
		return Program::create<TextInstance>(sstr.str());
        return nullptr;
    }


/**
Mixins of FileInstance
**/

std::string FileInstance::text() {
    return to_string(file_path);
}

bool FileInstance::boolean() {
    return to_boolean(file_path);
}

