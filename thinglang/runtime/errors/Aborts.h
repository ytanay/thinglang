#pragma once

#include <iostream>


enum AbortReason {
    EMPTY_PROGRAM_STACK,
    UNHANDLED_EXCEPTION
};


inline std::string format_abort_reason(AbortReason reason){
    switch(reason){
        case EMPTY_PROGRAM_STACK: return "Empty program stack";
        case UNHANDLED_EXCEPTION: return "Unhandled exception";
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
