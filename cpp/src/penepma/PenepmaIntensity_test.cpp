/**
 * @file
 *
 * @brief Tests the penepma intensity data structure.
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
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "penepma/PenepmaIntensity.h"
// Project headers
#include "Subshell.h"
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_PenepmaIntensity)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
     * @brief Test getTotalIntensity_1_sre method.
     */
    BOOST_AUTO_TEST_CASE(test_getTotalIntensity_1_sre)
    {
        PenepmaIntensity penepmaIntensity;
        penepmaIntensity.initial = Subshell::L1;
        penepmaIntensity.final = Subshell::M3;
        penepmaIntensity.energy_eV = 1.0228E+03;
        penepmaIntensity.primary_1_sre = 2.370269E-06;
        penepmaIntensity.primaryError_1_sre = 6.51E-09;
        penepmaIntensity.characteristicFluorescence_1_sre = 1.208609E-10;
        penepmaIntensity.characteristicFluorescenceError_1_sre = 4.50E-11;
        penepmaIntensity.bremsstrahlungFluorescence_1_sre = 2.961788E-09;
        penepmaIntensity.bremsstrahlungFluorescenceError_1_sre = 2.05E-10;
        penepmaIntensity.totalFluorescence_1_sre = 3.082649E-09;
        penepmaIntensity.totalFluorescenceError_1_sre = 2.50E-10;
        penepmaIntensity.total_1_sre = 2.373352E-06;
        penepmaIntensity.totalError_1_sre = 6.51E-09;

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
