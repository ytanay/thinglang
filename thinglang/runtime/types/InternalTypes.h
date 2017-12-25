/**
    InternalTypes.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#include "../../foundation/classes/containers/IteratorType.h"
#include "../../foundation/classes/containers/ListType.h"
#include "../../foundation/classes/containers/MapType.h"
#include "../../foundation/classes/exceptions/ExceptionType.h"
#include "../../foundation/classes/io/console/ConsoleType.h"
#include "../../foundation/classes/io/filesystem/DirectoryType.h"
#include "../../foundation/classes/io/filesystem/DirectoryEntryType.h"
#include "../../foundation/classes/io/filesystem/FileType.h"
#include "../../foundation/classes/types/BoolType.h"
#include "../../foundation/classes/types/NumberType.h"
#include "../../foundation/classes/types/TextType.h"
#include "../../foundation/classes/utilities/TimeType.h"

enum PrimitiveType {
    TEXT, NUMBER
};

inline Type get_type(const std::string& type_name){
    if(type_name == "iterator") return singleton<IteratorType>();
    if(type_name == "list") return singleton<ListType>();
    if(type_name == "map") return singleton<MapType>();
    if(type_name == "Exception") return singleton<ExceptionType>();
    if(type_name == "Console") return singleton<ConsoleType>();
    if(type_name == "Directory") return singleton<DirectoryType>();
    if(type_name == "DirectoryEntry") return singleton<DirectoryEntryType>();
    if(type_name == "File") return singleton<FileType>();
    if(type_name == "bool") return singleton<BoolType>();
    if(type_name == "number") return singleton<NumberType>();
    if(type_name == "text") return singleton<TextType>();
    if(type_name == "Time") return singleton<TimeType>();
    
    throw RuntimeError("Unknown type name: " + type_name);  
}
