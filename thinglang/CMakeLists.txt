
add_library(thingcore

        runtime/execution/Program.cpp

        foundation/classes/types/TextType.cpp
        foundation/classes/types/NumberType.cpp
        foundation/classes/types/BoolType.cpp
        foundation/classes/types/ObjectType.cpp
        foundation/classes/containers/ListType.cpp
        foundation/classes/containers/MapType.cpp
        foundation/classes/io/console/ConsoleType.cpp
        foundation/classes/io/filesystem/FileType.cpp
        foundation/classes/io/filesystem/DirectoryType.cpp
        foundation/classes/io/filesystem/DirectoryEntryType.cpp
        foundation/classes/utilities/TimeType.cpp
        foundation/classes/exceptions/ExceptionType.cpp
        foundation/classes/containers/IteratorType.cpp

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

