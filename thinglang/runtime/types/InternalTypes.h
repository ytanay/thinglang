/**
    InternalTypes.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#include "core/BoolType.h"
#include "core/ConsoleType.h"
#include "core/DirectoryType.h"
#include "core/DirectoryEntryType.h"
#include "core/ExceptionType.h"
#include "core/FileType.h"
#include "core/IteratorType.h"
#include "core/ListType.h"
#include "core/MapType.h"
#include "core/NumberType.h"
#include "core/TextType.h"
#include "core/TimeType.h"

enum PrimitiveType {
    TEXT, NUMBER
};

inline Type get_type(const std::string& type_name){
    if(type_name == "bool") return singleton<BoolType>();
    if(type_name == "Console") return singleton<ConsoleType>();
    if(type_name == "Directory") return singleton<DirectoryType>();
    if(type_name == "DirectoryEntry") return singleton<DirectoryEntryType>();
    if(type_name == "Exception") return singleton<ExceptionType>();
    if(type_name == "File") return singleton<FileType>();
    if(type_name == "iterator") return singleton<IteratorType>();
    if(type_name == "list") return singleton<ListType>();
    if(type_name == "map") return singleton<MapType>();
    if(type_name == "number") return singleton<NumberType>();
    if(type_name == "text") return singleton<TextType>();
    if(type_name == "Time") return singleton<TimeType>();
    
    throw RuntimeError("Unknown type name: " + type_name);  
}
