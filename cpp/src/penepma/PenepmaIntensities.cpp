/**
 * @file
 *
 * @brief Implementation of reading penepma intensities file.
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
#include "penepma/PenepmaIntensities.h"
// Project headers
#include "Subshell.h"
// Project private headers
#include "tools/tools_io.h"

// Global and constant variables/functions.

PenepmaIntensities::PenepmaIntensities(const boost::filesystem::path &filepath) : dataFilepath(filepath)
{

}

PenepmaIntensities::~PenepmaIntensities()
{

}

PenepmaIntensity PenepmaIntensities::getXrayIntensity(const int atomicNumber, const Subshell initial, const Subshell final)
{
    auto position = xrayIntensities.find(atomicNumber);
    if (position == xrayIntensities.end())
    {
        readData();
    }

    position = xrayIntensities.find(atomicNumber);
    if (position == xrayIntensities.end())
    {
        std::string message = "Cannot find data for the atomic number " + atomicNumber;
        throw std::out_of_range(message);
    }

    XrayIntensities xrayIntensities = position->second;
    for( auto& xrayIntensity : xrayIntensities)
    {
        if (xrayIntensity.initial == initial && xrayIntensity.final == final)
        {
            return xrayIntensity;
        }
    }

    std::string message = "Cannot find data for the intensity for these subshells " + label(initial) + " " + label(final);
    throw std::out_of_range(message);
}

XrayIntensities PenepmaIntensities::getXrayIntensity(const int atomicNumber, const Subshell initial)
{

}

XrayIntensities PenepmaIntensities::getXrayIntensity(const int atomicNumber)
{

}

void PenepmaIntensities::readData()
{
    assert(boost::filesystem::is_regular_file(dataFilepath));

    std::ifstream inputFile(dataFilepath.c_str(), std::ios::binary);
    if (!inputFile)
    {
        return;
    }

    xrayIntensities.clear();

    // Skip the first line.
    std::string line;
    std::getline (inputFile, line);

    const std::string seperatorKeyValue = " ";

    while(inputFile.good())
    {
        std::getline (inputFile, line);
        boost::trim(line);
        if (!line.empty())
        {
            std::vector<std::string> splitVector;
            boost::split(splitVector, line, boost::is_any_of(seperatorKeyValue), boost::token_compress_on);

            if(splitVector.empty() || splitVector.size() < 14)
            {
                continue;
            }

            if (splitVector.size() == 14) {
                const unsigned int atomicNumber = extractIntegerValueFromString(splitVector[0]);

                PenepmaIntensity penepmaIntensity;
                penepmaIntensity.initial = convert(splitVector[1]);
                penepmaIntensity.final = convert(splitVector[2]);
                penepmaIntensity.energy_eV = extractDoubleValueFromString(splitVector[3]);
                penepmaIntensity.primary_1_sre = extractDoubleValueFromString(splitVector[4]);
                penepmaIntensity.primaryError_1_sre = extractDoubleValueFromString(splitVector[5]);
                penepmaIntensity.characteristicFluorescence_1_sre = extractDoubleValueFromString(splitVector[6]);
                penepmaIntensity.characteristicFluorescenceError_1_sre = extractDoubleValueFromString(splitVector[7]);
                penepmaIntensity.bremsstrahlungFluorescence_1_sre = extractDoubleValueFromString(splitVector[8]);
                penepmaIntensity.bremsstrahlungFluorescenceError_1_sre = extractDoubleValueFromString(splitVector[9]);
                penepmaIntensity.totalFluorescence_1_sre = extractDoubleValueFromString(splitVector[10]);
                penepmaIntensity.totalFluorescenceError_1_sre = extractDoubleValueFromString(splitVector[11]);
                penepmaIntensity.total_1_sre = extractDoubleValueFromString(splitVector[12]);
                penepmaIntensity.totalError_1_sre = extractDoubleValueFromString(splitVector[13]);

                if (xrayIntensities.count(atomicNumber) == 0)
                {
                    xrayIntensities.insert(std::make_pair(atomicNumber, XrayIntensities()));
                }
                auto position = xrayIntensities.find(atomicNumber);
                position->second.push_back(penepmaIntensity);
            }
        }
    }

    inputFile.close();
}
