/**
 * @file
 * @brief This file defines a macro to create a test and run it
 * Note: this macro defines the main() function
 * \ingroup testlib
 */
#ifndef R_UNIT_TESTLIB_TESTLIB_MAIN_HPP_
#define R_UNIT_TESTLIB_TESTLIB_MAIN_HPP_

#include "test_func.hpp"


/** Define the main function and use it to test a given function */
#define UNITTEST_DEFINE_MAIN_TEST(TFUNC)                                                          \
    /** Main function: test TFUNC */                                                              \
    int main() {                                                                                  \
        using namespace UnitTest::TestLib;                                                        \
        original_bk = Utils::Log::Backend::get();                                                 \
        original_sty = Utils::Log::Style::get();                                                  \
        Utils::Error::Claricpp::toggle_backtrace(true);                                           \
        return test_func((TFUNC));                                                                \
    }


#endif
