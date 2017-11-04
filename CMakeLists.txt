cmake_minimum_required(VERSION 3.7)
set(CMAKE_CXX_STANDARD 14)

project(thinglang)

set(CMAKE_EXE_LINKER_FLAGS "-static-libstdc++ -static-libgcc")

enable_testing()

add_subdirectory(thinglang)
add_subdirectory(tests)

add_test(all_tests thingtests)
