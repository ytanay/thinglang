#pragma once

#include "../../../../runtime/utils/TypeNames.h"


class DirectoryInstance : public BaseThingInstance {
    
    public:
    explicit DirectoryInstance() = default; // empty constructor
    
    explicit DirectoryInstance(std::string file_path) : file_path(std::move(file_path)) {}; // value constructor
    
    /** Mixins **/
    
    std::string text() override;
    bool boolean() override;

    
    /** Members **/
    std::string file_path;

	~DirectoryInstance() override = default;

};


class DirectoryType : public ThingTypeInternal {
    
    public:
	DirectoryType() : ThingTypeInternal({ &__constructor__, &contents}) {};
 
	static void __constructor__();
	static void contents();

    
};
