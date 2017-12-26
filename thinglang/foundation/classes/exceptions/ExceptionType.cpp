#include "../../../runtime/types/InternalTypes.h"


void ExceptionType::__constructor__() {
    auto self = Program::create<ExceptionInstance>();
    auto message = Program::argument<TextInstance>();

    self->message = message;
}


std::string ExceptionInstance::text() {
    return "Exception: " + message->text();
}

bool ExceptionInstance::boolean() {
    return true;
}

InternalType ExceptionInstance::type() const {
    return singleton<ExceptionType>();
}

Things ExceptionInstance::children() {
    return {message};
}

