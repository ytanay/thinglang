/**
    FileType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../execution/Globals.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"




class FileInstance : public BaseThingInstance {
    
    public:
    explicit FileInstance() = default; // empty constructor
    
    explicit FileInstance(std::string file_path, std::fstream file) : file_path(file_path) {}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override;
    virtual bool boolean() override;

    
    /** Members **/
    std::string file_path;
std::fstream file;
    
    
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
