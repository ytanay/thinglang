#pragma once

#include <string>
#include <algorithm>

template <typename T>
inline std::string to_string(T val){
    return std::to_string(val);
}

inline std::string to_string(std::string val){
    return val;
}

inline std::string to_string(bool val){
    return val ? "true" : "false";
}

template <typename T>
inline bool to_boolean(T val){
    return val != 0;
}

inline bool to_boolean(const std::string &val){
    return val.length() > 0;
}

inline std::string trim(std::string str){
    auto it = std::find_if(str.begin(), str.end(), [](char ch){
        return !std::isspace<char>(ch , std::locale::classic());
    });

    str.erase(str.begin(), it);
    return str;
}