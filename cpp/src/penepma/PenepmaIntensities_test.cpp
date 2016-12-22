/**
 * @file
 *
 * @brief Tests reading penepma intensities file.
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
#include <boost/filesystem.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "penepma/PenepmaIntensities.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_PenepmaIntensities)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
    * @brief Test the code to find the data file pe-intens-05.dat.
    */
    BOOST_AUTO_TEST_CASE(test_find_data_file)
    {
        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-intens-05.dat";
        BOOST_CHECK_EQUAL(true, boost::filesystem::is_regular_file(dataFilepath));

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test getXrayIntensity method.
     */
    BOOST_AUTO_TEST_CASE(test_getXrayIntensity)
    {
        const double tolerance = 0.001;

        PenepmaIntensity penepmaIntensityRef;
        penepmaIntensityRef.initial = Subshell::L1;
        penepmaIntensityRef.final = Subshell::M3;
        penepmaIntensityRef.energy_eV = 1.0228E+03;
        penepmaIntensityRef.primary_1_sre = 2.370269E-06;
        penepmaIntensityRef.primaryError_1_sre = 6.51E-09;
        penepmaIntensityRef.characteristicFluorescence_1_sre = 1.208609E-10;
        penepmaIntensityRef.characteristicFluorescenceError_1_sre = 4.50E-11;
        penepmaIntensityRef.bremsstrahlungFluorescence_1_sre = 2.961788E-09;
        penepmaIntensityRef.bremsstrahlungFluorescenceError_1_sre = 2.05E-10;
        penepmaIntensityRef.totalFluorescence_1_sre = 3.082649E-09;
        penepmaIntensityRef.totalFluorescenceError_1_sre = 2.50E-10;
        penepmaIntensityRef.total_1_sre = 2.373352E-06;
        penepmaIntensityRef.totalError_1_sre = 6.51E-09;

        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-intens-05.dat";
        PenepmaIntensities penepmaIntensities(dataFilepath);

        PenepmaIntensity penepmaIntensity = penepmaIntensities.getXrayIntensity(29, Subshell::L1, Subshell::M3);

        BOOST_CHECK_EQUAL(penepmaIntensityRef.initial, penepmaIntensity.initial);
        BOOST_CHECK_EQUAL(penepmaIntensityRef.final, penepmaIntensity.final);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.energy_eV, penepmaIntensity.energy_eV, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.primary_1_sre, penepmaIntensity.primary_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.primaryError_1_sre, penepmaIntensity.primaryError_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.characteristicFluorescence_1_sre, penepmaIntensity.characteristicFluorescence_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.characteristicFluorescenceError_1_sre, penepmaIntensity.characteristicFluorescenceError_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.bremsstrahlungFluorescence_1_sre, penepmaIntensity.bremsstrahlungFluorescence_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.bremsstrahlungFluorescenceError_1_sre, penepmaIntensity.bremsstrahlungFluorescenceError_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.totalFluorescence_1_sre, penepmaIntensity.totalFluorescence_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.totalFluorescenceError_1_sre, penepmaIntensity.totalFluorescenceError_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.total_1_sre, penepmaIntensity.total_1_sre, tolerance);
        BOOST_CHECK_CLOSE(penepmaIntensityRef.totalError_1_sre, penepmaIntensity.totalError_1_sre, tolerance);

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
