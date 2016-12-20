/**
 * @file
 *
 * @brief Tests for the AtomicTransitions class.
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
#include <exception>
// Library headers
#include <boost/test/unit_test.hpp>
#include <boost/filesystem.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "AtomicTransitions.h"
#include "XrayTransition.h"
#include "Subshell.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_AtomicTransitions)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
 * Test the method getXrayTransition.
 */
BOOST_AUTO_TEST_CASE(test_getXrayTransition)
{
    const double tolerance = 0.001;

    AtomicTransitions atomicTransitions;

    BOOST_CHECK_THROW(atomicTransitions.getXrayTransition(5, Subshell::K, Subshell::L2), std::out_of_range);
    BOOST_CHECK_THROW(atomicTransitions.getXrayTransition(100, Subshell::K, Subshell::L2), std::out_of_range);

    BOOST_CHECK_THROW(atomicTransitions.getXrayTransition(6, Subshell::K, Subshell::L1), std::out_of_range);
    BOOST_CHECK_THROW(atomicTransitions.getXrayTransition(6, Subshell::L3, Subshell::K), std::out_of_range);
    BOOST_CHECK_THROW(atomicTransitions.getXrayTransition(6, Subshell::L3, Subshell::M5), std::out_of_range);

    XrayTransition xrayTransitionRef;
    xrayTransitionRef.energy_eV = 2.82020E+02;
    xrayTransitionRef.initial = Subshell::K;
    xrayTransitionRef.final = Subshell::L2;
    xrayTransitionRef.probability = 5.61488E-04;
    xrayTransitionRef.fraction = 0.333804176713780344;

    XrayTransition xrayTransition = atomicTransitions.getXrayTransition(6, Subshell::K, Subshell::L2);

    BOOST_CHECK_CLOSE(xrayTransitionRef.energy_eV, xrayTransition.energy_eV, tolerance);
    BOOST_CHECK_EQUAL(xrayTransitionRef.initial, xrayTransition.initial);
    BOOST_CHECK_EQUAL(xrayTransitionRef.final, xrayTransition.final);
    BOOST_CHECK_CLOSE(xrayTransitionRef.probability, xrayTransition.probability, tolerance);
    BOOST_CHECK_CLOSE(xrayTransitionRef.fraction, xrayTransition.fraction, tolerance);

    xrayTransitionRef.energy_eV = 2.82030E+02;
    xrayTransitionRef.initial = Subshell::K;
    xrayTransitionRef.final = Subshell::L3;
    xrayTransitionRef.probability = 1.12060E-03;
    xrayTransitionRef.fraction = 0.6661958232862966;

    xrayTransition = atomicTransitions.getXrayTransition(6, Subshell::K, Subshell::L3);

    BOOST_CHECK_CLOSE(xrayTransitionRef.energy_eV, xrayTransition.energy_eV, tolerance);
    BOOST_CHECK_EQUAL(xrayTransitionRef.initial, xrayTransition.initial);
    BOOST_CHECK_EQUAL(xrayTransitionRef.final, xrayTransition.final);
    BOOST_CHECK_CLOSE(xrayTransitionRef.probability, xrayTransition.probability, tolerance);
    BOOST_CHECK_CLOSE(xrayTransitionRef.fraction, xrayTransition.fraction, tolerance);

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
     * @brief Test the code to find the data file pdrelax.p11.
     */
    BOOST_AUTO_TEST_CASE(test_find_data_file)
    {
        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "data/pdrelax.p11";
        BOOST_CHECK_EQUAL(true, boost::filesystem::is_regular_file(dataFilepath));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
