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

inline Type create_type(const std::string& type_name){
    if(type_name == "bool") return new BoolType();
    if(type_name == "Console") return new ConsoleType();
    if(type_name == "Directory") return new DirectoryType();
    if(type_name == "DirectoryEntry") return new DirectoryEntryType();
    if(type_name == "Exception") return new ExceptionType();
    if(type_name == "File") return new FileType();
    if(type_name == "iterator") return new IteratorType();
    if(type_name == "list") return new ListType();
    if(type_name == "map") return new MapType();
    if(type_name == "number") return new NumberType();
    if(type_name == "text") return new TextType();
    if(type_name == "Time") return new TimeType();
    
    throw RuntimeError("Unknown type name: " + type_name);  
}
