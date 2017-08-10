//
// Created by Yotam on 5/13/2017.
//

#pragma once

#include <string>
#include <exception>
#include <utility>

class RuntimeError : public std::exception {
public:
    explicit RuntimeError(std::string message) : message(std::move(message)) {};

    const char *what() const noexcept override;


private:
    std::string message;
};
