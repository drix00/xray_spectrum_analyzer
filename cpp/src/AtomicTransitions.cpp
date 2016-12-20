/**
 * @file
 *
 * @brief Implementation of atomic transitions.
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
#include <cassert>
#include <exception>
// Library headers
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "AtomicTransitions.h"
// Project headers
#include "XrayTransition.h"
#include "Subshell.h"
// Project private headers

// Global and constant variables/functions.

AtomicTransitions::AtomicTransitions()
{

}

AtomicTransitions::~AtomicTransitions()
{

}

XrayTransition AtomicTransitions::getXrayTransition(const int atomicNumber, const Subshell initial, const Subshell final)
{
    auto position = atomicXrayTransitions.find(atomicNumber);
    if (position == atomicXrayTransitions.end())
    {
        readData();
    }

    position = atomicXrayTransitions.find(atomicNumber);
    if (position == atomicXrayTransitions.end())
    {
        std::string message = "Cannot find data for the atomic number " + atomicNumber;
        throw std::out_of_range(message);
    }

    XrayTransitions xrayTransitions = position->second;
    for( auto& xrayTransition : xrayTransitions)
    {
        if (xrayTransition.initial == initial && xrayTransition.final == final)
        {
            return xrayTransition;
        }
    }

    std::string message = "Cannot find data for the transition for these subshells " + label(initial) + " " + label(final);
    throw std::out_of_range(message);
}

std::vector<XrayTransition> AtomicTransitions::getXrayTransitions(const int atomicNumber, const Subshell initial)
{

}

std::vector<XrayTransition> AtomicTransitions::getXrayTransitions(const int atomicNumber)
{

}

void AtomicTransitions::readData()
{
    boost::filesystem::path currentPath = boost::filesystem::current_path();
    boost::filesystem::path dataFilepath = currentPath / "data/pdrelax.p11";
    assert(boost::filesystem::is_regular_file(dataFilepath));

    std::ifstream inputFile(dataFilepath.c_str(), std::ios::binary);
    if (!inputFile)
    {
        return;
    }

    atomicXrayTransitions.clear();
    atomicAugerTransitions.clear();

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

            if(splitVector.empty() || splitVector.size() < 6)
            {
                continue;
            }

            if (splitVector.size() == 6) {
                const unsigned int atomicNumber = extractIntegerValueFromString(splitVector[0]);

                const Subshell initial = convert(extractIntegerValueFromString(splitVector[1]));

                const Subshell intermediate = convert(extractIntegerValueFromString(splitVector[2]));

                const int final_value = extractIntegerValueFromString(splitVector[3]);
                Subshell final;
                if (final_value != 0)
                {
                    final = convert(final_value);
                } else
                {
                    final = intermediate;
                }

                const double probability = extractDoubleValueFromString(splitVector[4]);
                const double energy_eV = extractDoubleValueFromString(splitVector[5]);

                if(final_value == 0)
                {
                    XrayTransition xrayTransition;
                    xrayTransition.initial = initial;
                    xrayTransition.final = final;
                    xrayTransition.probability = probability;
                    xrayTransition.energy_eV = energy_eV;
                    xrayTransition.fraction = 0.0;

                    if (atomicXrayTransitions.count(atomicNumber) == 0)
                    {
                        atomicXrayTransitions.insert(std::make_pair(atomicNumber, XrayTransitions()));
                    }
                    auto position = atomicXrayTransitions.find(atomicNumber);
                    position->second.push_back(xrayTransition);
                }
                else
                {
                    AugerTransition augerTransition;
                    augerTransition.initial = initial;
                    augerTransition.intermediate = intermediate;
                    augerTransition.final = final;
                    augerTransition.probability = probability;
                    augerTransition.energy_eV = energy_eV;

                    if (atomicAugerTransitions.count(atomicNumber) == 0)
                    {
                        atomicAugerTransitions.insert(std::make_pair(atomicNumber, AugerTransitions()));
                    }
                    auto position = atomicAugerTransitions.find(atomicNumber);
                    position->second.push_back(augerTransition);
                }

            }
        }
    }

    inputFile.close();
    computeXrayLineFraction();
}

double AtomicTransitions::extractDoubleValueFromString(std::string &itemStr)
{
    boost::trim(itemStr);
    const std::string stringValue = itemStr;
    const double value = boost::lexical_cast<double>(stringValue);
    return value;
}

int AtomicTransitions::extractIntegerValueFromString(std::string &itemStr)
{
    boost::trim(itemStr);
    const std::string stringValue = itemStr;
    const int value = boost::lexical_cast<int>(stringValue);
    return value;
}

void AtomicTransitions::computeXrayLineFraction()
{
    for (auto& element : atomicXrayTransitions)
    {
        // Do K shell.
        double total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellK(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellK(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do L shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellL(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellL(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do M shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellM(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellM(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do N shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellN(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellN(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do O shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellO(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellO(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do P shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellP(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellP(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

        // Do Q shell.
        total = 0.0;
        for (auto& xrayTransition : element.second)
        {
            if (isShellQ(xrayTransition.initial))
            {
                total += xrayTransition.probability;
            }
        }

        for (auto& xrayTransition : element.second)
        {
            if (isShellQ(xrayTransition.initial))
            {
                xrayTransition.fraction = xrayTransition.probability / total;
            }
        }

    }
}
