cmake_minimum_required(VERSION 3.7)
project(thinglang)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        thinglang/runtime/main.cpp
        thinglang/runtime/loader/ProgramReader.cpp

        thinglang/runtime/containers/MethodDefinition.cpp

        thinglang/runtime/execution/Program.cpp

        )

set(CMAKE_EXE_LINKER_FLAGS "-static")
add_executable(thinglang ${SOURCE_FILES})
