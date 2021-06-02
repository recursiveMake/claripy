/**
 * @file
 * @brief This file defines a group of create methods for trivial passthrough string ops
 */
#ifndef R_CREATE_STRING_TRIVIAL_HPP_
#define R_CREATE_STRING_TRIVIAL_HPP_

#include "../private/binary.hpp"
#include "../private/uint_binary.hpp"
#include "../private/unary.hpp"


namespace Create::String {

    /********************************************************************/
    /*                   Unary Passthrough Functions                    */
    /********************************************************************/

    /** Create a bool Expression with an String::IsDigit op */
    inline EBasePtr is_digit(const EBasePtr &x, SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::unary<Ex::Bool, Ex::String, Op::String::IsDigit, Ex::String>(x, std::move(sp));
    }

    /********************************************************************/
    /*                 Int Binary Passthrough Functions                 */
    /********************************************************************/

    /** Create an Expression with an String::SignExt op
     *  Note: Currently Ints are taken in as BVs
     */
    inline EBasePtr to_int(const EBasePtr &expr, const Constants::UInt integer,
                           SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::uint_binary<Constants::UInt, Ex::BV, Ex::String, Op::String::ToInt,
                               CP::SizeMode::Second, Ex::String>(expr, integer, std::move(sp));
    }

    /** Create an Expression with an String::Len op
     *  Note: Currently Ints are output as BVs
     */
    inline EBasePtr len(const EBasePtr &expr, const Constants::UInt integer, SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::uint_binary<Constants::UInt, Ex::BV, Ex::String, Op::String::Len,
                               CP::SizeMode::Second, Ex::String>(expr, integer, std::move(sp));
    }

    /********************************************************************/
    /*                   Binary Passthrough Functions                   */
    /********************************************************************/

    /** Create an Expression with a String::Contains op */
    inline EBasePtr contains(const EBasePtr &left, const EBasePtr &right, SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::binary<Ex::Bool, Ex::String, Op::String::Contains, CP::SizeMode::NA,
                          Ex::String>(left, right, std::move(sp));
    }

    /** Create an Expression with a String::PrefixOf op */
    inline EBasePtr prefix_of(const EBasePtr &left, const EBasePtr &right, SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::binary<Ex::Bool, Ex::String, Op::String::PrefixOf, CP::SizeMode::NA,
                          Ex::String>(left, right, std::move(sp));
    }

    /** Create an Expression with a String::SuffixOf op */
    inline EBasePtr suffix_of(const EBasePtr &left, const EBasePtr &right, SPAV &&sp = nullptr) {
        namespace Ex = Expression;
        namespace CP = ::Create::Private;
        return CP::binary<Ex::Bool, Ex::String, Op::String::SuffixOf, CP::SizeMode::NA,
                          Ex::String>(left, right, std::move(sp));
    }

} // namespace Create::String

#endif