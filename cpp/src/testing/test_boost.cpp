/**
 * @file
 *
 * @brief Tests for boost library.
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
#include <boost/test/unit_test.hpp>
#include <boost/version.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
// Project headers
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_boost)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE( test_is_working )
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
 * @brief Test version 1.49.
 */
BOOST_AUTO_TEST_CASE( test_version_1_49 )
{
    BOOST_CHECK_NE("1_49", BOOST_LIB_VERSION);

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
 * @brief Test version 1.54.
 */
BOOST_AUTO_TEST_CASE( test_version_1_54 )
{
#ifdef _WIN32
    BOOST_CHECK_NE("1_54", BOOST_LIB_VERSION);
#else
        BOOST_CHECK_NE("1_54", BOOST_LIB_VERSION);
#endif

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
 * @brief Test version 1.55.
 */
BOOST_AUTO_TEST_CASE(test_version_1_55)
    {
#ifdef _WIN32
    BOOST_CHECK_NE("1_55", BOOST_LIB_VERSION);
#else
    BOOST_CHECK_NE("1_55", BOOST_LIB_VERSION);
#endif

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
    }

/**
 * @brief Test version 1.60.
 */
BOOST_AUTO_TEST_CASE(test_version_1_60)
{
#ifdef _WIN32
    BOOST_CHECK_EQUAL("1_60", BOOST_LIB_VERSION);
#else
        BOOST_CHECK_EQUAL("1_60", BOOST_LIB_VERSION);
#endif

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

BOOST_AUTO_TEST_SUITE_END()
