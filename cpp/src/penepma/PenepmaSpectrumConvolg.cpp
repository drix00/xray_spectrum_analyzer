/**
 * @file
 *
 * @brief Implementation of reading penepma convoluted spectrum file.
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
#include <string>
// Library headers
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "penepma/PenepmaSpectrumConvolg.h"
// Project headers
// Project private headers
#include "tools/tools_io.h"
#include "tools/tools_data.h"

// Global and constant variables/functions.

PenepmaSpectrumConvolg::PenepmaSpectrumConvolg(const boost::filesystem::path &filepath) : dataFilepath(filepath)
{
    energies_eV.reserve(1000);
    intensities_1_eVsre.reserve(1000);
}

PenepmaSpectrumConvolg::~PenepmaSpectrumConvolg()
{
    energies_eV.clear();
    intensities_1_eVsre.clear();
}

Energies_eV PenepmaSpectrumConvolg::getEnergies_eV()
{
    if (energies_eV.empty())
    {
        readData();
    }

    return energies_eV;
}

Intensities_1_eVsre PenepmaSpectrumConvolg::getIntensities_1_eVsre()
{
    if (intensities_1_eVsre.empty())
    {
        readData();
    }

    return intensities_1_eVsre;
}

void PenepmaSpectrumConvolg::readData()
{
    assert(boost::filesystem::is_regular_file(dataFilepath));

    std::ifstream inputFile(dataFilepath.c_str(), std::ios::binary);
    if (!inputFile)
    {
        return;
    }

    energies_eV.clear();
    intensities_1_eVsre.clear();

    const std::string seperatorKeyValue = " ";

    while(inputFile.good())
    {
        std::string line;
        std::getline (inputFile, line);
        boost::trim(line);
        if (!line.empty())
        {
            std::vector<std::string> splitVector;
            boost::split(splitVector, line, boost::is_any_of(seperatorKeyValue), boost::token_compress_on);

            if(splitVector.empty() || splitVector.size() < 2)
            {
                continue;
            }

            if (splitVector.size() == 2)
            {
                const double energy_eV = extractDoubleValueFromString(splitVector[0]);
                const double intensity_1_eVsre = extractDoubleValueFromString(splitVector[1]);

                energies_eV.push_back(energy_eV);
                intensities_1_eVsre.push_back(intensity_1_eVsre);
            }
        }
    }

    inputFile.close();
}
