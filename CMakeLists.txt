cmake_minimum_required(VERSION 3.7)
project(thinglang)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        thinglang/runtime/main.cpp
        thinglang/runtime/containers/MethodDefinition.cpp
        thinglang/runtime/containers/ThingInstance.cpp

        thinglang/runtime/errors/RuntimeError.cpp

        thinglang/runtime/execution/Program.cpp
        thinglang/runtime/execution/Symbol.cpp

        thinglang/runtime/loader/ProgramReader.cpp

        thinglang/runtime/types/NoneType.cpp
        thinglang/runtime/types/NumberInstance.cpp
        thinglang/runtime/types/TextInstance.cpp
        thinglang/runtime/types/TypeInfo.cpp

        thinglang/runtime/builtins/BuiltinOutput.cpp
       )

set(CMAKE_EXE_LINKER_FLAGS "-static")
add_executable(thinglang ${SOURCE_FILES})
