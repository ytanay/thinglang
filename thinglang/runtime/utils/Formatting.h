#pragma once

#include <string>

template <typename T>
inline std::string to_string(T val){
    return std::to_string(val);
}

inline std::string to_string(std::string val){
    return val;
}

template <typename T>
inline bool to_boolean(T val){
    return val != 0;
}

inline bool to_boolean(const std::string &val){
    return val.length() > 0;
}