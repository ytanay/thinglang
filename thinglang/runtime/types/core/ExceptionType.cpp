#include "../InternalTypes.h"
#include "../../execution/Program.h"


void ExceptionType::__constructor__() {
    auto message = Program::argument<TextInstance>();
    auto self = Program::create<ExceptionInstance>();

    self->message = message;
}


std::string ExceptionInstance::text() {
    return message->text();
}

bool ExceptionInstance::boolean() {
    return true;
}

Type ExceptionInstance::type() const {
    return singleton<ExceptionType>();
}

