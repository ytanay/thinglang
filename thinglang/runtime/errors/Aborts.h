#pragma once

#include <iostream>

#include "../utils/TypeNames.h"
#include "../execution/Program.h"


enum AbortReason {
    EMPTY_PROGRAM_STACK,
    MISSING_RETURN
};


inline std::string format_abort_reason(AbortReason reason){
    switch(reason){
        case EMPTY_PROGRAM_STACK: return "Empty program stack";
        case MISSING_RETURN: return "Method ended without returning";
    }
}


inline void critical_abort(AbortReason reason){
    std::cerr << std::endl << std::endl;
    std::cerr << "THINGLANG VM ERROR: CRITICAL ABORT" << std::endl;
    std::cerr << "==================================" << std::endl << std::endl;
    std::cerr << "The thinglang runtime environment has detected an irrecoverable error while running the program." << std::endl;
    std::cerr << "Abort reason: " << format_abort_reason(reason) << " (" << std::to_string(reason) << ")" << std::endl;

    std::exit(1);
}
