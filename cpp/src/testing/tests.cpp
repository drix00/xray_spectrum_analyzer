/**
 * @file
 *
 * @brief Create the main for running the project tests.
 *
 * Also used to test if the unit test framework is working.
 * The code can be used as skeleton for new test files.
 * Just remember to not redefine BOOST_TEST_MODULE, which create the main entry for running the tests.
 *
 * @note This file does not use precompiled header with \#pragma hdrstop
 * because BOOST_TEST_MODULE have to be define before including the unit_test header.
 *
 * @author Hendrix Demers <hendrix.demers@mail.mcgill.ca>
 * @since 1.0
 */

// Copyright 2016 Hendrix Demers
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

// C system headers
// C++ system header
// Library headers
/**
 * Define the name of the test module.
 */
#define BOOST_TEST_MODULE testing_xray_spectrum_analyzer

#if !defined( WIN32 )
    /**
     * Use dynamic linking when now using visual studio.
     */
    #define BOOST_TEST_DYN_LINK
#endif

/**
 * Use boost test to detect memory leak.
 */
#define BOOST_TEST_DETECT_MEMORY_LEAK
#include <boost/test/unit_test.hpp>
// Precompiled header
// Current declaration header file of this implementation file.
// Project headers
// Project private headers

BOOST_AUTO_TEST_SUITE(tests)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE( test_is_working )
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

BOOST_AUTO_TEST_SUITE_END()
