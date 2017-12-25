#pragma once

#include "../../utils/TypeNames.h"
#include "TextType.h"
#include "../../execution/Program.h"


class DirectoryEntryInstance : public BaseThingInstance {
    
    public:
    explicit DirectoryEntryInstance() = default; // empty constructor
    explicit DirectoryEntryInstance(TextInstance* path, TextInstance* type) : path(path), type(type) {};
    explicit DirectoryEntryInstance(std::string path, unsigned int type) : path(Program::create<TextInstance>(path)),
                                                                           type(Program::create<TextInstance>(parse_type(type))) {};
    
    std::string text() override;
    bool boolean() override;

    static std::string parse_type(unsigned int type);

    Thing get(Index index) override;

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
