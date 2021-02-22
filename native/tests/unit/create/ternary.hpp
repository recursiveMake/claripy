/**
 * @file
 * @brief Trivial ternary create test
 * \ingroup unittest
 */
#ifndef __TESTS_UNIT_CREATE_TERNARY_HPP__
#define __TESTS_UNIT_CREATE_TERNARY_HPP__

#include "create.hpp"
#include "dcast.hpp"
#include "testlib.hpp"


/** SizeMode shortcut */
using SM = Create::Private::SizeMode;


/** Test a ternary op */
template <typename Out, typename In, typename OpT, SM Mode, auto CreateF> inline void ternary() {
    static_assert(Utils::is_ancestor<Expression::Base, Out>,
                  "ternary requires Out be an Expression");
    static_assert(Utils::is_ancestor<Expression::Base, In>,
                  "ternary requires In be an Expression");
    static_assert(Op::is_ternary<OpT>, "ternary requires a ternary OpT");
    if constexpr (Utils::is_ancestor<Expression::Bits, Out>) {
        const constexpr bool sized_in { Utils::is_ancestor<Expression::Bits, In> };
        static_assert(Utils::TD::boolean<sized_in, In>,
                      "ternary does not suppot sized output types without sized input types");
    }

    // Create distinct inputs
    const auto a { UnitTest::TestLib::Factories::t_literal<In>(0) };
    const auto b { UnitTest::TestLib::Factories::t_literal<In>(1) };
    const auto c { UnitTest::TestLib::Factories::t_literal<In>(2) };

    // Test
    const auto exp { CreateF(Create::EAnVec {}, a, b, c) };

    // Pointer checks
    UNITTEST_ASSERT(a.use_count() == 2)
    UNITTEST_ASSERT(b.use_count() == 2)
    UNITTEST_ASSERT(c.use_count() == 2)
    UNITTEST_ASSERT(exp->op.use_count() == 1)

    // Type check
    const auto ternary { dcast<OpT>(exp->op) };
    const auto exp_down { dcast<Out>(exp) };
    const auto a_down { dcast<In>(a) };
    const auto b_down { dcast<In>(b) };
    const auto c_down { dcast<In>(c) };

    // Contains check
    UNITTEST_ASSERT(ternary->first == a)
    UNITTEST_ASSERT(ternary->second == b)
    UNITTEST_ASSERT(ternary->third == c)

    // Size test
    if constexpr (Utils::is_ancestor<Expression::Bits, Out>) {
        // Because of previous static asserts we know In must also be sized
        Constants::UInt new_bit_length { a_down->bit_length };
        if constexpr (Mode == SM::Add) {
            new_bit_length += b_down->bit_length + c_down->bit_length;
        }
        else {
            static_assert(Utils::TD::false_<Mode>, "Unsupported mode for ternary");
        }
        UNITTEST_ASSERT(exp_down->bit_length == new_bit_length)
    }
}

/** A specialization where In = Out */
template <typename InOut, typename OpT, SM Mode, auto CreateF> inline void ternary() {
    ternary<InOut, InOut, OpT, Mode, CreateF>();
}

#endif