#pragma once

#include <string>
#include <sstream>
#include <ostream>
#include <algorithm>
#include <iterator>

#include "../types/infrastructure/ThingInstance.h"

template <typename T>
inline std::string to_string(T val){
    return std::to_string(val);
}

template <typename T>
inline std::string to_string(std::vector<T> lst){
    if(lst.size() == 0)
        return "[]";

    std::stringstream stream;
    std::copy(lst.begin(), lst.end(), std::ostream_iterator<T>(stream, ", "));

    auto result = stream.str();

    result.erase(result.size() - 2);

    return "[" + result + "]";
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

template <typename T>
inline bool to_boolean(std::vector<T> lst){
    return lst.size() > 0;
}

inline std::string trim(std::string str){
    auto it = std::find_if(str.begin(), str.end(), [](char ch){
        return !std::isspace<char>(ch , std::locale::classic());
    });

    str.erase(str.begin(), it);
    return str;
}

inline std::ostream &operator<<(std::ostream &os, const Thing& thing){
    return os << thing->text();
}

inline int to_number(std::string str){
    return atoi(str.c_str());
}