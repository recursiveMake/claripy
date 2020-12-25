/** @file */
#include "abstract_base.hpp"

#include "../../../errors/unexpected.hpp"

// For brevity
using namespace Utils::Log::Style;


AbstractBase::AbstractBase() {}

// Disallow usage
std::string AbstractBase::operator()(const Level &, std::ostringstream &) const {
    throw Errors::Unexpected::IncorrectUsage("This function should not be possible to call");
}