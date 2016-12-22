/**
 * @file
 *
 * @brief Implementation of the functions to help reading and writing file for the projects.
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
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "tools/tools_io.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

double extractDoubleValueFromString(std::string &itemStr)
{
    boost::trim(itemStr);
    const std::string stringValue = itemStr;
    const double value = boost::lexical_cast<double>(stringValue);
    return value;
}

int extractIntegerValueFromString(std::string &itemStr)
{
    boost::trim(itemStr);
    const std::string stringValue = itemStr;
    const int value = boost::lexical_cast<int>(stringValue);
    return value;
}

