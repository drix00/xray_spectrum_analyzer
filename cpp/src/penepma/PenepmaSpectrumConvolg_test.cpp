/**
 * @file
 *
 * @brief Tests reading penepma convoluted spectrum file.
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
#include "penepma/PenepmaSpectrumConvolg.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

BOOST_AUTO_TEST_SUITE(test_PenepmaSpectrumConvolg)

/**
 * @brief Test if this testcase file is included in the testsuite and run.
 */
BOOST_AUTO_TEST_CASE(test_is_working)
{
    //BOOST_FAIL( "Nothing to test" );
    BOOST_CHECK(true);
}

    /**
    * @brief Test the code to find the data file chspect-05.dat.
    */
    BOOST_AUTO_TEST_CASE(test_find_data_file)
    {
        boost::filesystem::path currentPath = boost::filesystem::current_path();
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/chspect-05.dat";
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
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/chspect-05.dat";
        PenepmaSpectrumConvolg spectrum = PenepmaSpectrumConvolg(dataFilepath);
        Energies_eV energies_eV = spectrum.getEnergies_eV();
        const int numberPointsRef = 3150;
        BOOST_CHECK_EQUAL(numberPointsRef, energies_eV.size());

        BOOST_CHECK_CLOSE(1.00000E+01, energies_eV[0], tolerance);
        BOOST_CHECK_CLOSE(8.01000E+03, energies_eV[1601-1], tolerance);
        BOOST_CHECK_CLOSE(1.57550E+04, energies_eV[numberPointsRef-1], tolerance);

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
        boost::filesystem::path dataFilepath = currentPath / "test_data/penepma/cu_15kV/chspect-05.dat";
        PenepmaSpectrumConvolg spectrum = PenepmaSpectrumConvolg(dataFilepath);
        Intensities_1_eVsre intensities_1_eVsre = spectrum.getIntensities_1_eVsre();
        const int numberPointsRef = 3150;
        BOOST_CHECK_EQUAL(numberPointsRef, intensities_1_eVsre.size());

        BOOST_CHECK_CLOSE(1.00000E-25, intensities_1_eVsre[0], tolerance);
        BOOST_CHECK_CLOSE(1.89679E-07, intensities_1_eVsre[1601-1], tolerance);
        BOOST_CHECK_CLOSE(1.00000E-25, intensities_1_eVsre[numberPointsRef-1], tolerance);

        //BOOST_FAIL( "Nothing to test" );
        BOOST_CHECK(true);
    }

BOOST_AUTO_TEST_SUITE_END()
