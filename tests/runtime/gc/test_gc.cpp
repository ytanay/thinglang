#define CATCH_CONFIG_MAIN
#include "../../include/catch.h"
#include "../../../thinglang/runtime/types/core/ListType.h"
#include "../../../thinglang/runtime/types/core/TextType.h"


TEST_CASE( "Full flow GC test", "[gc]" ) {


    REQUIRE(Program::object_count() == 0);

    Thing text1 = Program::create<TextInstance>("Hello World!");
    Thing text2 = Program::create<TextInstance>("Goodbye World!");
    std::vector<Thing> things = {text1, text2};

    Thing list1 = Program::create<ListInstance>(things);

    REQUIRE(Program::object_count() == 3);

    Program::create_frame(1);
    Program::frame()[0] = list1;

    Program::mark();
    Program::sweep();

    REQUIRE(Program::object_count() == 3);

    Program::push(list1);
    ListType::pop();
    Program::pop();

    Program::mark();
    Program::sweep();

    REQUIRE(Program::object_count() == 2);

    Program::push(list1);
    ListType::pop();
    Program::pop();

    Program::mark();
    Program::sweep();

    REQUIRE(Program::object_count() == 1);

}