/**
    DirectoryType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "TextType.h"
#include "../../utils/Formatting.h"
#include "../../execution/Program.h"


class DirectoryEntryInstance : public BaseThingInstance {
    
    public:
    explicit DirectoryEntryInstance() = default; // empty constructor
    explicit DirectoryEntryInstance(TextInstance* path, TextInstance* type) : path(path), type(type) {};
    explicit DirectoryEntryInstance(std::string path, unsigned int type) : path(Program::create<TextInstance>(path)),
                                                                           type(Program::create<TextInstance>(parse_type(type))) {};
    
    std::string text() override;
    bool boolean() override;

    static std::string parse_type(unsigned int type){
        return to_string(type);
    }


    TextInstance* path{};
    TextInstance* type{};

	~DirectoryEntryInstance() override = default;

    Things children() override;

};


class DirectoryEntryType : public ThingTypeInternal {
    
    public:
    DirectoryEntryType() : ThingTypeInternal({ &__constructor__}) {};
 
	static void __constructor__();
};