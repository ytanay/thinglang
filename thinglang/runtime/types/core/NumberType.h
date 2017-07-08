#pragma once

#include "../../utils/TypeNames.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ArgumentList.h"


class NumberInstance : public ThingInstance {
public:

    NumberInstance() : val(0) {};
    NumberInstance(double val) : val(val) {};

    double val = 0;
};


class NumberType : public ThingType<NumberInstance> {
public:
    NumberType() : ThingType({&add}) {};


    static Thing add(ArgumentList& args){
        auto lhs = args.get<0, NumberInstance>();
        auto rhs = args.get<1, NumberInstance>();
        return Thing(new NumberInstance(lhs->val + rhs->val));
    }
};