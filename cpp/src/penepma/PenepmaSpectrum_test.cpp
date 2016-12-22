/**
 * @file
 *
 * @brief Tests for PenepmaSpectrum class.
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
#include "penepma/PenepmaSpectrum.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_PenepmaSpectrum)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

/**
* @brief Test the code to find the data file pe-spect-05.dat.
*/
BOOST_AUTO_TEST_CASE(test_find_data_file)
{
    boost::filesystem::path currentPath = boost::filesystem::current_path();
    boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-spect-05.dat";
    BOOST_CHECK_EQUAL(true, boost::filesystem::is_regular_file(dataFilepath));

    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
     * @brief Test getEnergies_eV method.
     */
    BOOST_AUTO_TEST_CASE(test_getEnergies_eV)
    {
        const double tolerance = 0.001;

        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-spect-05.dat";
        PenepmaSpectrum spectrum = PenepmaSpectrum(dataFilepath);
        Energies_eV energies_eV = spectrum.getEnergies_eV();
        const int numberPointsRef = 1000;
        BOOST_CHECK_EQUAL(numberPointsRef, energies_eV.size());

        BOOST_CHECK_CLOSE(7.500001E+00, energies_eV[0], tolerance);
        BOOST_CHECK_CLOSE(7.492501E+03, energies_eV[500-1], tolerance);
        BOOST_CHECK_CLOSE(1.499250E+04, energies_eV[numberPointsRef-1], tolerance);

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test getIntensities_1_eVsre method.
     */
    BOOST_AUTO_TEST_CASE(test_getIntensities_1_eVsre)
    {
        const double tolerance = 0.001;

        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-spect-05.dat";
        PenepmaSpectrum spectrum = PenepmaSpectrum(dataFilepath);
        Intensities_1_eVsre intensities_1_eVsre = spectrum.getIntensities_1_eVsre();
        const int numberPointsRef = 1000;
        BOOST_CHECK_EQUAL(numberPointsRef, intensities_1_eVsre.size());

        BOOST_CHECK_CLOSE(1.000000E-35, intensities_1_eVsre[0], tolerance);
        BOOST_CHECK_CLOSE(5.493100E-09, intensities_1_eVsre[500-1], tolerance);
        BOOST_CHECK_CLOSE(4.063026E-11, intensities_1_eVsre[numberPointsRef-1], tolerance);

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

    /**
     * @brief Test getIntensitiesError_1_eVsre method.
     */
    BOOST_AUTO_TEST_CASE(test_getIntensitiesError_1_eVsre)
    {
        const double tolerance = 0.001;

        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/pe-spect-05.dat";
        PenepmaSpectrum spectrum = PenepmaSpectrum(dataFilepath);
        Intensities_1_eVsre intensityErrors_1_eVsre = spectrum.getIntensityErrors_1_eVsre();
        const int numberPointsRef = 1000;
        BOOST_CHECK_EQUAL(numberPointsRef, intensityErrors_1_eVsre.size());

        BOOST_CHECK_CLOSE(1.000000E-35, intensityErrors_1_eVsre[0], tolerance);
        BOOST_CHECK_CLOSE(7.685423E-11, intensityErrors_1_eVsre[500-1], tolerance);
        BOOST_CHECK_CLOSE(7.198716E-12, intensityErrors_1_eVsre[numberPointsRef-1], tolerance);

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
