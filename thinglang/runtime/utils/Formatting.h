#pragma once

#include <string>

template <typename T>
inline std::string to_string(T val){
    return std::to_string(val);
}

inline std::string to_string(std::string val){
    return val;
}