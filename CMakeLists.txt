cmake_minimum_required(VERSION 3.7)
project(thinglang)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES
        thinglang/runtime/main.cpp
        thinglang/runtime/loader/ProgramReader.cpp

        thinglang/runtime/containers/Method.cpp

        thinglang/runtime/execution/Program.cpp


        thinglang/runtime/errors/RuntimeError.cpp

        thinglang/runtime/execution/Opcodes.h
        thinglang/runtime/execution/Symbol.cpp

        thinglang/runtime/types/core/NumberType.h
        thinglang/runtime/types/core/TextType.h
        thinglang/runtime/types/core/OutputType.h

        thinglang/runtime/types/infrastructure/ThingInstance.cpp
        thinglang/runtime/types/infrastructure/ThingType.cpp

        thinglang/runtime/types/InternalTypes.h

        thinglang/runtime/utils/Formatting.h
        thinglang/runtime/utils/TypeNames.h
        thinglang/runtime/errors/Aborts.h)

set(CMAKE_EXE_LINKER_FLAGS "-static")
add_executable(thinglang ${SOURCE_FILES})
