#clude_directories(${CTEST_SOURCE_DIRECTORY}/thinglang)

add_executable(thingtests runtime/gc/test_gc.cpp)
target_link_libraries(thingtests thingcore)