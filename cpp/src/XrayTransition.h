#ifndef X_RAY_SPECTRUM_ANALYZER_XRAYTRANSITION_H
#define X_RAY_SPECTRUM_ANALYZER_XRAYTRANSITION_H

/**
 * @file
 *
 * @brief Atomic x-ray transition data.
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
// Library headers
// Project headers
#include "Subshell.h"
// Project private headers

/**
 * @brief Atomic x-ray transition.
 */
class XrayTransition {
public:
    /// Initial subshell of the x-ray transition.
    Subshell initial;
    /// Final subshell if the x-ray transition.
    Subshell final;
    /// Probability of the x-ray transition.
    double probability;
    /// Energy of the x-ray transition in eV.
    double energy_eV;
    /// X-ray line fraction based on the initial subshell.
    double fraction;
};

#endif //X_RAY_SPECTRUM_ANALYZER_XRAYTRANSITION_H
