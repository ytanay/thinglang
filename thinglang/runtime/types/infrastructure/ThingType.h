#pragma once

#include "../../utils/TypeNames.h"
#include "ArgumentList.h"

class ThingInstance {};

template <typename THING_TYPE>
class ThingType {
public:
    ThingType(LocalMethods methods) : methods(methods) {};

    Thing call(Index idx, ArgumentList& args){
        return methods[idx](args);
    }

    std::shared_ptr<THING_TYPE> create(){
        return std::shared_ptr<THING_TYPE>(new THING_TYPE());
    }



private:
    LocalMethods methods;
};