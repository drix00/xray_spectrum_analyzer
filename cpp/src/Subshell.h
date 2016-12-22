#ifndef SUBSHELL_H
#define SUBSHELL_H

/**
 * @file
 *
 * @brief Defined the subshells used in this project.
 *
 * Subshells are taken from PENELOPE manual.
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
#include <iosfwd>
// C system headers
// C++ system header
#include <string>
// Library headers
// Project headers
// Project private headers

/**
 * @brief Subshell enumeration.
 *
 * The Subshell::K start at 1 to have the same value than in PENELOPE code.
 *
 * @since 1.0
 */
enum class Subshell
{
    K=1,
    L1, L2, L3,
    M1, M2, M3, M4, M5,
    N1, N2, N3, N4, N5, N6, N7,
    O1, O2, O3, O4, O5, O6, O7,
    P1, P2, P3, P4, P5,
    Q1,
    OUTER
};

/**
 * @brief Convert an integer to the corresponding Subshell.
 *
 * @since 1.0
 *
 * @param[in] subshell_number
 * @return a subshell
 */
Subshell convert(const int subshell_number);

/**
 * @brief Convert a string to the corresponding Subshell.
 *
 * @since 1.0
 *
 * @param[in] subshell_number
 * @return a subshell
 */
Subshell convert(const std::string &subshell_str);

/**
 * @brief Convert a Subshell into it string representation.
 *
 * @since 1.0
 *
 * @param[in] subshell
 * @return string representation of the subshell
 */
std::string label(const Subshell subshell);

/**
 * @brief Get the orbital string of a Subshell.
 *
 * @since 1.0
 *
 * @param[in] subshell
 * @return oribtal string
 */
std::string orbital(const Subshell subshell);

/**
 * @brief Write a Subshell into a stream.
 *
 * @since 1.0
 *
 * @param[in,out] stream output stream
 * @param[in] subshell
 * @return output stream
 */
std::ostream& operator << (std::ostream& stream, const Subshell subshell);

bool isShellK(const Subshell subshell);
bool isShellL(const Subshell subshell);
bool isShellM(const Subshell subshell);
bool isShellN(const Subshell subshell);
bool isShellO(const Subshell subshell);
bool isShellP(const Subshell subshell);
bool isShellQ(const Subshell subshell);

#endif // SUBSHELL_H
