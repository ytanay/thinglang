#pragma once

#include <utility>

#include "../../utils/TypeNames.h"

struct MethodInfo {
    Index address, frame_size;
};

class ThingTypeUser {
public:
    explicit ThingTypeUser(std::vector<MethodInfo> methods) : methods(std::move(methods)) {};
    inline MethodInfo method(Index idx) const {
        return methods[idx];
    };


    std::vector<MethodInfo> methods;
};


class ThingTypeInternal {
public:
    explicit ThingTypeInternal(InternalMethods methods) : methods(std::move(methods)) {};

    inline void call(Index idx) {
        methods[idx]();
    };


private:
    InternalMethods methods;
};