
add_library(thingcore

        runtime/execution/Program.cpp

        runtime/types/core/TextType.cpp
        runtime/types/core/NumberType.cpp
        runtime/types/core/BoolType.cpp
        runtime/types/core/ListType.cpp
        runtime/types/core/MapType.cpp
        runtime/types/core/ConsoleType.cpp
        runtime/types/core/FileType.cpp
        runtime/types/core/DirectoryType.cpp
        runtime/types/core/DirectoryEntryType.cpp
        runtime/types/core/TimeType.cpp
        runtime/types/core/ExceptionType.cpp
        runtime/types/core/IteratorType.cpp

        runtime/types/interfaces/IndexedInterface.h

        runtime/errors/RuntimeError.cpp

        runtime/execution/Opcodes.h
        runtime/execution/Instruction.cpp

        runtime/loader/ProgramReader.cpp

        runtime/types/infrastructure/ThingInstance.cpp
        runtime/types/infrastructure/ThingType.cpp
        runtime/types/infrastructure/Comparisons.cpp

        runtime/types/InternalTypes.h

        runtime/utils/Formatting.h
        runtime/utils/TypeNames.h
        runtime/utils/Containers.h
        runtime/errors/Aborts.h

        include/args.h
        runtime/execution/Globals.h)


add_executable(thinglang runtime/main.cpp)
target_link_libraries (thinglang thingcore)

