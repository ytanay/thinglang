add_executable(thingtests runtime/gc/test_gc.cpp)
target_link_libraries(thingtests thingcore)
add_test(all_tests thingtests)

