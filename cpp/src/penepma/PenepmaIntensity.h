#ifndef X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITY_H
#define X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITY_H

/**
 * @file
 *
 * @brief Penepma intensity data structure.
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

class PenepmaIntensity {
public:
    PenepmaIntensity();
    ~PenepmaIntensity();

public:
    /// Initial subshell of the x-ray transition.
    Subshell initial;
    /// Final subshell if the x-ray transition.
    Subshell final;
    /// Energy of the x-ray transition in eV.
    double energy_eV;
    /// Primary photons (from electron interactions).
    double primary_1_sre;
    /// Flourescence from characteristic x rays.
    double characteristicFluorescence_1_sre;
    /// Flourescence from bremsstrahlung quanta.
    double bremsstrahlungFluorescence_1_sre;
    /// Total fluorescence.
    double totalFluorescence_1_sre;
    /// Statistical uncertainty (3 sigma) for primary photons (from electron interactions).
    double primaryError_1_sre;
    /// Statistical uncertainty (3 sigma) for flourescence from characteristic x rays.
    double characteristicFluorescenceError_1_sre;
    /// Statistical uncertainty (3 sigma) for flourescence from bremsstrahlung quanta.
    double bremsstrahlungFluorescenceError_1_sre;
    /// Statistical uncertainty (3 sigma) for total fluorescence.
    double totalFluorescenceError_1_sre;
    /// Total intensity.
    double total_1_sre;
    /// Statistical uncertainty (3 sigma) for total intensity.
    double totalError_1_sre;
};

#endif //X_RAY_SPECTRUM_ANALYZER_PENEPMAINTENSITY_H
