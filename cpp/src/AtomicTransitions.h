#ifndef X_RAY_SPECTRUM_ANALYZER_ATOMICTRANSITIONS_H
#define X_RAY_SPECTRUM_ANALYZER_ATOMICTRANSITIONS_H

/**
 * @file
 *
 * @brief Atomic transitions data.
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
// Project headers
#include "XrayTransition.h"
#include "AugerTransition.h"
#include "Subshell.h"
// Project private headers

class AtomicTransitions {
public:
    AtomicTransitions();
    ~AtomicTransitions();

    XrayTransition getXrayTransition(const int atomicNumber, const Subshell initial, const Subshell final);
    std::vector<XrayTransition> getXrayTransitions(const int atomicNumber, const Subshell initial);
    std::vector<XrayTransition> getXrayTransitions(const int atomicNumber);

private:
    void readData();
    double extractDoubleValueFromString(std::string &itemStr);
    int extractIntegerValueFromString(std::string &itemStr);
    void computeXrayLineFraction();

private:
    using XrayTransitions = std::vector<XrayTransition>;
    using AugerTransitions = std::vector<AugerTransition>;

    std::unordered_map<int, XrayTransitions> atomicXrayTransitions;
    std::unordered_map<int, AugerTransitions> atomicAugerTransitions;
};


#endif //X_RAY_SPECTRUM_ANALYZER_ATOMICTRANSITIONS_H
