#ifndef X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITIES_H
#define X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITIES_H

/**
 * @file
 *
 * @brief Read penepma intensities file.
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

// Forwards declarations
// C system headers
// C++ system header
#include <vector>
#include <unordered_map>
// Library headers
#include <boost/filesystem.hpp>
// Project headers
#include "Subshell.h"
// Project private headers
#include "penepma/PenepmaIntensity.h"

using XrayIntensities = std::vector<PenepmaIntensity>;

class PenepmaIntensities {
public:
    PenepmaIntensities(const boost::filesystem::path &filepath);
    ~PenepmaIntensities();

    PenepmaIntensity getXrayIntensity(const int atomicNumber, const Subshell initial, const Subshell final);
    XrayIntensities getXrayIntensity(const int atomicNumber, const Subshell initial);
    XrayIntensities getXrayIntensity(const int atomicNumber);

private:
    void readData();

private:
    boost::filesystem::path dataFilepath;

    std::unordered_map<int, XrayIntensities> xrayIntensities;
};

#endif //X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITIES_H
