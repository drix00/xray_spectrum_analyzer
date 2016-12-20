/**
 * @file
 *
 * @brief Tests for Subshell enumerations and related functions.
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
#include <vector>
// Library  headers
#include <boost/test/unit_test.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "Subshell.h"
// Project headers
// Project private headers

// Global and constant variables/functions.


BOOST_AUTO_TEST_SUITE(test_subshell)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
 * @brief Test the conversion to integer.
 */
BOOST_AUTO_TEST_CASE(test_integer_conversion)
{
    BOOST_CHECK_EQUAL(1, static_cast<int>(Subshell::K));

    BOOST_CHECK_EQUAL(2, static_cast<int>(Subshell::L1));
    BOOST_CHECK_EQUAL(3, static_cast<int>(Subshell::L2));
    BOOST_CHECK_EQUAL(4, static_cast<int>(Subshell::L3));

    BOOST_CHECK_EQUAL(5, static_cast<int>(Subshell::M1));
    BOOST_CHECK_EQUAL(6, static_cast<int>(Subshell::M2));
    BOOST_CHECK_EQUAL(7, static_cast<int>(Subshell::M3));
    BOOST_CHECK_EQUAL(8, static_cast<int>(Subshell::M4));
    BOOST_CHECK_EQUAL(9, static_cast<int>(Subshell::M5));

    BOOST_CHECK_EQUAL(10, static_cast<int>(Subshell::N1));
    BOOST_CHECK_EQUAL(11, static_cast<int>(Subshell::N2));
    BOOST_CHECK_EQUAL(12, static_cast<int>(Subshell::N3));
    BOOST_CHECK_EQUAL(13, static_cast<int>(Subshell::N4));
    BOOST_CHECK_EQUAL(14, static_cast<int>(Subshell::N5));
    BOOST_CHECK_EQUAL(15, static_cast<int>(Subshell::N6));
    BOOST_CHECK_EQUAL(16, static_cast<int>(Subshell::N7));

    BOOST_CHECK_EQUAL(17, static_cast<int>(Subshell::O1));
    BOOST_CHECK_EQUAL(18, static_cast<int>(Subshell::O2));
    BOOST_CHECK_EQUAL(19, static_cast<int>(Subshell::O3));
    BOOST_CHECK_EQUAL(20, static_cast<int>(Subshell::O4));
    BOOST_CHECK_EQUAL(21, static_cast<int>(Subshell::O5));
    BOOST_CHECK_EQUAL(22, static_cast<int>(Subshell::O6));
    BOOST_CHECK_EQUAL(23, static_cast<int>(Subshell::O7));

    BOOST_CHECK_EQUAL(24, static_cast<int>(Subshell::P1));
    BOOST_CHECK_EQUAL(25, static_cast<int>(Subshell::P2));
    BOOST_CHECK_EQUAL(26, static_cast<int>(Subshell::P3));
    BOOST_CHECK_EQUAL(27, static_cast<int>(Subshell::P4));
    BOOST_CHECK_EQUAL(28, static_cast<int>(Subshell::P5));

    BOOST_CHECK_EQUAL(29, static_cast<int>(Subshell::Q1));

    BOOST_CHECK_EQUAL(30, static_cast<int>(Subshell::OUTER));

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}
    /**
     * @brief Test the integer conversion.
     */
    BOOST_AUTO_TEST_CASE(test_subshell_conversion)
    {
        BOOST_CHECK_EQUAL(Subshell::K, static_cast<Subshell>(1));

        BOOST_CHECK_EQUAL(Subshell::L1, static_cast<Subshell>(2));
        BOOST_CHECK_EQUAL(Subshell::L2, static_cast<Subshell>(3));
        BOOST_CHECK_EQUAL(Subshell::L3, static_cast<Subshell>(4));

        BOOST_CHECK_EQUAL(Subshell::M1, static_cast<Subshell>(5));
        BOOST_CHECK_EQUAL(Subshell::M2, static_cast<Subshell>(6));
        BOOST_CHECK_EQUAL(Subshell::M3, static_cast<Subshell>(7));
        BOOST_CHECK_EQUAL(Subshell::M4, static_cast<Subshell>(8));
        BOOST_CHECK_EQUAL(Subshell::M5, static_cast<Subshell>(9));

        BOOST_CHECK_EQUAL(Subshell::N1, static_cast<Subshell>(10));
        BOOST_CHECK_EQUAL(Subshell::N2, static_cast<Subshell>(11));
        BOOST_CHECK_EQUAL(Subshell::N3, static_cast<Subshell>(12));
        BOOST_CHECK_EQUAL(Subshell::N4, static_cast<Subshell>(13));
        BOOST_CHECK_EQUAL(Subshell::N5, static_cast<Subshell>(14));
        BOOST_CHECK_EQUAL(Subshell::N6, static_cast<Subshell>(15));
        BOOST_CHECK_EQUAL(Subshell::N7, static_cast<Subshell>(16));

        BOOST_CHECK_EQUAL(Subshell::O1, static_cast<Subshell>(17));
        BOOST_CHECK_EQUAL(Subshell::O2, static_cast<Subshell>(18));
        BOOST_CHECK_EQUAL(Subshell::O3, static_cast<Subshell>(19));
        BOOST_CHECK_EQUAL(Subshell::O4, static_cast<Subshell>(20));
        BOOST_CHECK_EQUAL(Subshell::O5, static_cast<Subshell>(21));
        BOOST_CHECK_EQUAL(Subshell::O6, static_cast<Subshell>(22));
        BOOST_CHECK_EQUAL(Subshell::O7, static_cast<Subshell>(23));

        BOOST_CHECK_EQUAL(Subshell::P1, static_cast<Subshell>(24));
        BOOST_CHECK_EQUAL(Subshell::P2, static_cast<Subshell>(25));
        BOOST_CHECK_EQUAL(Subshell::P3, static_cast<Subshell>(26));
        BOOST_CHECK_EQUAL(Subshell::P4, static_cast<Subshell>(27));
        BOOST_CHECK_EQUAL(Subshell::P5, static_cast<Subshell>(28));

        BOOST_CHECK_EQUAL(Subshell::Q1, static_cast<Subshell>(29));

        BOOST_CHECK_EQUAL(Subshell::OUTER, static_cast<Subshell>(30));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test the convertion to integer using the convert function.
     */
    BOOST_AUTO_TEST_CASE(test_convert)
    {
        BOOST_CHECK_EQUAL(Subshell::K, convert(1));

        BOOST_CHECK_EQUAL(Subshell::L1, convert(2));
        BOOST_CHECK_EQUAL(Subshell::L2, convert(3));
        BOOST_CHECK_EQUAL(Subshell::L3, convert(4));

        BOOST_CHECK_EQUAL(Subshell::M1, convert(5));
        BOOST_CHECK_EQUAL(Subshell::M2, convert(6));
        BOOST_CHECK_EQUAL(Subshell::M3, convert(7));
        BOOST_CHECK_EQUAL(Subshell::M4, convert(8));
        BOOST_CHECK_EQUAL(Subshell::M5, convert(9));

        BOOST_CHECK_EQUAL(Subshell::N1, convert(10));
        BOOST_CHECK_EQUAL(Subshell::N2, convert(11));
        BOOST_CHECK_EQUAL(Subshell::N3, convert(12));
        BOOST_CHECK_EQUAL(Subshell::N4, convert(13));
        BOOST_CHECK_EQUAL(Subshell::N5, convert(14));
        BOOST_CHECK_EQUAL(Subshell::N6, convert(15));
        BOOST_CHECK_EQUAL(Subshell::N7, convert(16));

        BOOST_CHECK_EQUAL(Subshell::O1, convert(17));
        BOOST_CHECK_EQUAL(Subshell::O2, convert(18));
        BOOST_CHECK_EQUAL(Subshell::O3, convert(19));
        BOOST_CHECK_EQUAL(Subshell::O4, convert(20));
        BOOST_CHECK_EQUAL(Subshell::O5, convert(21));
        BOOST_CHECK_EQUAL(Subshell::O6, convert(22));
        BOOST_CHECK_EQUAL(Subshell::O7, convert(23));

        BOOST_CHECK_EQUAL(Subshell::P1, convert(24));
        BOOST_CHECK_EQUAL(Subshell::P2, convert(25));
        BOOST_CHECK_EQUAL(Subshell::P3, convert(26));
        BOOST_CHECK_EQUAL(Subshell::P4, convert(27));
        BOOST_CHECK_EQUAL(Subshell::P5, convert(28));

        BOOST_CHECK_EQUAL(Subshell::Q1, convert(29));

        BOOST_CHECK_EQUAL(Subshell::OUTER, convert(30));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test the label function.
     */
    BOOST_AUTO_TEST_CASE(test_label)
    {
        BOOST_CHECK_EQUAL("K", label(Subshell::K));

        BOOST_CHECK_EQUAL("L1", label(Subshell::L1));
        BOOST_CHECK_EQUAL("L2", label(Subshell::L2));
        BOOST_CHECK_EQUAL("L3", label(Subshell::L3));

        BOOST_CHECK_EQUAL("M1", label(Subshell::M1));
        BOOST_CHECK_EQUAL("M2", label(Subshell::M2));
        BOOST_CHECK_EQUAL("M3", label(Subshell::M3));
        BOOST_CHECK_EQUAL("M4", label(Subshell::M4));
        BOOST_CHECK_EQUAL("M5", label(Subshell::M5));

        BOOST_CHECK_EQUAL("N1", label(Subshell::N1));
        BOOST_CHECK_EQUAL("N2", label(Subshell::N2));
        BOOST_CHECK_EQUAL("N3", label(Subshell::N3));
        BOOST_CHECK_EQUAL("N4", label(Subshell::N4));
        BOOST_CHECK_EQUAL("N5", label(Subshell::N5));
        BOOST_CHECK_EQUAL("N6", label(Subshell::N6));
        BOOST_CHECK_EQUAL("N7", label(Subshell::N7));

        BOOST_CHECK_EQUAL("O1", label(Subshell::O1));
        BOOST_CHECK_EQUAL("O2", label(Subshell::O2));
        BOOST_CHECK_EQUAL("O3", label(Subshell::O3));
        BOOST_CHECK_EQUAL("O4", label(Subshell::O4));
        BOOST_CHECK_EQUAL("O5", label(Subshell::O5));
        BOOST_CHECK_EQUAL("O6", label(Subshell::O6));
        BOOST_CHECK_EQUAL("O7", label(Subshell::O7));

        BOOST_CHECK_EQUAL("P1", label(Subshell::P1));
        BOOST_CHECK_EQUAL("P2", label(Subshell::P2));
        BOOST_CHECK_EQUAL("P3", label(Subshell::P3));
        BOOST_CHECK_EQUAL("P4", label(Subshell::P4));
        BOOST_CHECK_EQUAL("P5", label(Subshell::P5));

        BOOST_CHECK_EQUAL("Q1", label(Subshell::Q1));

        BOOST_CHECK_EQUAL("Outer", label(Subshell::OUTER));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test the orbital function.
     */
    BOOST_AUTO_TEST_CASE(test_orbital)
    {
        BOOST_CHECK_EQUAL("1s1/2", orbital(Subshell::K));

        BOOST_CHECK_EQUAL("2s1/2", orbital(Subshell::L1));
        BOOST_CHECK_EQUAL("2p1/2", orbital(Subshell::L2));
        BOOST_CHECK_EQUAL("2p3/2", orbital(Subshell::L3));

        BOOST_CHECK_EQUAL("3s1/2", orbital(Subshell::M1));
        BOOST_CHECK_EQUAL("3p1/2", orbital(Subshell::M2));
        BOOST_CHECK_EQUAL("3p3/2", orbital(Subshell::M3));
        BOOST_CHECK_EQUAL("3d3/2", orbital(Subshell::M4));
        BOOST_CHECK_EQUAL("3d5/2", orbital(Subshell::M5));

        BOOST_CHECK_EQUAL("4s1/2", orbital(Subshell::N1));
        BOOST_CHECK_EQUAL("4p1/2", orbital(Subshell::N2));
        BOOST_CHECK_EQUAL("4p3/2", orbital(Subshell::N3));
        BOOST_CHECK_EQUAL("4d3/2", orbital(Subshell::N4));
        BOOST_CHECK_EQUAL("4d5/2", orbital(Subshell::N5));
        BOOST_CHECK_EQUAL("4f5/2", orbital(Subshell::N6));
        BOOST_CHECK_EQUAL("4f7/2", orbital(Subshell::N7));

        BOOST_CHECK_EQUAL("5s1/2", orbital(Subshell::O1));
        BOOST_CHECK_EQUAL("5p1/2", orbital(Subshell::O2));
        BOOST_CHECK_EQUAL("5p3/2", orbital(Subshell::O3));
        BOOST_CHECK_EQUAL("5d3/2", orbital(Subshell::O4));
        BOOST_CHECK_EQUAL("5d5/2", orbital(Subshell::O5));
        BOOST_CHECK_EQUAL("5f5/2", orbital(Subshell::O6));
        BOOST_CHECK_EQUAL("5f7/2", orbital(Subshell::O7));

        BOOST_CHECK_EQUAL("6s1/2", orbital(Subshell::P1));
        BOOST_CHECK_EQUAL("6p1/2", orbital(Subshell::P2));
        BOOST_CHECK_EQUAL("6p3/2", orbital(Subshell::P3));
        BOOST_CHECK_EQUAL("6d3/2", orbital(Subshell::P4));
        BOOST_CHECK_EQUAL("6d5/2", orbital(Subshell::P5));

        BOOST_CHECK_EQUAL("7s1/2", orbital(Subshell::Q1));

        BOOST_CHECK_EQUAL("", orbital(Subshell::OUTER));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test isXShell methods.
     */
    BOOST_AUTO_TEST_CASE(test_isXShell)
    {
        std::vector<Subshell> shellKs = {Subshell::K};
        std::vector<Subshell> shellLs = {Subshell::L1, Subshell::L2, Subshell::L3};
        std::vector<Subshell> shellMs = {Subshell::M1, Subshell::M2, Subshell::M3, Subshell::M4, Subshell::M5};
        std::vector<Subshell> shellNs = {Subshell::N1, Subshell::N2, Subshell::N3, Subshell::N4, Subshell::N5, Subshell::N6, Subshell::N7};
        std::vector<Subshell> shellOs = {Subshell::O1, Subshell::O2, Subshell::O3, Subshell::O4, Subshell::O5, Subshell::O6, Subshell::O7};
        std::vector<Subshell> shellPs = {Subshell::P1, Subshell::P2, Subshell::P3, Subshell::P4, Subshell::P5};
        std::vector<Subshell> shellQs = {Subshell::Q1};

        for( auto subshell : shellKs)
        {
            BOOST_CHECK_EQUAL(true, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellLs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(true, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellMs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(true, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellNs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(true, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellOs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(true, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellPs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(true, isShellP(subshell));
            BOOST_CHECK_EQUAL(false, isShellQ(subshell));
        }

        for( auto subshell : shellQs)
        {
            BOOST_CHECK_EQUAL(false, isShellK(subshell));
            BOOST_CHECK_EQUAL(false, isShellL(subshell));
            BOOST_CHECK_EQUAL(false, isShellM(subshell));
            BOOST_CHECK_EQUAL(false, isShellN(subshell));
            BOOST_CHECK_EQUAL(false, isShellO(subshell));
            BOOST_CHECK_EQUAL(false, isShellP(subshell));
            BOOST_CHECK_EQUAL(true, isShellQ(subshell));
        }

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
