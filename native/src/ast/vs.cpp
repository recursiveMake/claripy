/** @file */
#include "vs.hpp"


// Return the name of the type this class represents
std::string AST::Cached::VS::fundamental_type_name() const {
    return "AST::VS";
}

/** @todo make this actually work */
AST::Hash AST::Cached::VS::hash(const Ops::Operation o, const Constants::Int length) {
    return Hash(o);
}
