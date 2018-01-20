#pragma once

#include "../../../../runtime/utils/TypeNames.h"


class FileInstance : public BaseThingInstance {
    
    public:
    explicit FileInstance() = default; // empty constructor
    
    explicit FileInstance(std::string file_path) : file_path(std::move(file_path)) {}; // value constructor
    
    std::string text() override;
    bool boolean() override;

    std::string file_path;
	std::fstream file;

    void open(std::string mode);

	~FileInstance() override {
		if(this->file.is_open()){
            this->file.close();
        }
	};

};


class FileType : public ThingTypeInternal {
    
    public:
    FileType() : ThingTypeInternal({ &__constructor__, &__construct_and_open__, &open, &close, &write, &read, &modify_time}) {}; // constructor
 
	static void __constructor__();
	static void __construct_and_open__();
	static void open();
	static void close();
	static void write();
	static void read();
	static void modify_time();
    
};
