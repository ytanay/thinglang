/**
    FileType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"


class FileInstance : public BaseThingInstance {
    
    public:
    explicit FileInstance() = default; // empty constructor
    
    explicit FileInstance(std::string file_path) : file_path(std::move(file_path)) {}; // value constructor
    
    /** Mixins **/
    
    std::string text() override;
    bool boolean() override;

    
    /** Members **/
    std::string file_path;
	std::fstream file;

	~FileInstance() override = default;

};


class FileType : public ThingTypeInternal {
    
    public:
    FileType() : ThingTypeInternal({ &__constructor__, &open, &close, &write, &read }) {}; // constructor
 
	static void __constructor__();
	static void open();
	static void close();
	static void write();
	static void read();
    
};
