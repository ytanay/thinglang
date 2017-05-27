//
// Created by Yotam on 5/13/2017.
//

#pragma once

#include <string>
#include <exception>

class RuntimeError : public std::exception {
public:
    RuntimeError(const std::string &message) : message(message), std::exception() {};

    virtual const char *what() const noexcept override {
        return message.c_str();
    }


private:
    std::string message;
};
