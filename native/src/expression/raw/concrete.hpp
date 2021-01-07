/**
 * @file
 * @brief
 */
#ifndef __EXPRESSION_RAW_CONCRETE_HPP__
#define __EXPRESSION_RAW_CONCRETE_HPP__

#include "base.hpp"


namespace Expression::Raw {

    struct Concrete : virtual public Base {
        virtual ~Concrete() = 0;
    };

} // namespace Expression::Raw

#endif