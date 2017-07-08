#pragma once

#include "../../utils/TypeNames.h"

class ArgumentList {
public:
    template <Index I, typename T>
    std::shared_ptr<T> get(){
        return std::static_pointer_cast<T>(args[I]);
    };

    void append(Thing t){
        args.push_back(t);
    }



private:
    std::vector<Thing> args;
};
