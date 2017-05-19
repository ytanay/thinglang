cmake_minimum_required(VERSION 3.7)
project(thingc)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        main.cpp
        containers/MethodDefinition.cpp
        containers/ThingInstance.cpp

        errors/RuntimeError.cpp

        execution/Program.cpp
        execution/Symbol.cpp

        loader/ProgramReader.cpp

        types/NoneType.cpp
        types/NumberInstance.cpp
        types/TextInstance.cpp
        types/TypeInfo.cpp builtins/BuiltinOutput.cpp builtins/BuiltinOutput.h)



add_executable(thingc ${SOURCE_FILES})
