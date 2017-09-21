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
        thinglang/runtime/execution/Instruction.cpp

        thinglang/runtime/types/core/TextType.cpp
        thinglang/runtime/types/core/NumberType.cpp
        thinglang/runtime/types/core/BoolType.cpp
        thinglang/runtime/types/core/ListType.cpp
        thinglang/runtime/types/core/ConsoleType.cpp

        thinglang/runtime/types/infrastructure/ThingInstance.cpp
        thinglang/runtime/types/infrastructure/ThingType.cpp

        thinglang/runtime/types/InternalTypes.h

        thinglang/runtime/utils/Formatting.h
        thinglang/runtime/utils/TypeNames.h
        thinglang/runtime/errors/Aborts.h

        thinglang/include/args.h
        thinglang/runtime/execution/Globals.h)


add_executable(thinglang ${SOURCE_FILES})
