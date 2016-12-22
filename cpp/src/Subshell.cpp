/**
 * @file
 *
 * @brief Implementation if the Subshell functions.
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
// Precompiled header
#pragma hdrstop
// Current declaration header file of this implementation file.
#include "Subshell.h"
// Project headers
// Project private headers

// Global and constant variables/functions.

Subshell convert(const int subshell_number)
{
    return static_cast<Subshell>(subshell_number);
}

Subshell convert(const std::string &subshell_str)
{
        if ( subshell_str == "K") return Subshell::K;
        if ( subshell_str == "L1") return Subshell::L1;
        if ( subshell_str == "L2") return Subshell::L2;
        if ( subshell_str == "L3") return Subshell::L3;
        if ( subshell_str == "M1") return Subshell::M1;
        if ( subshell_str == "M2") return Subshell::M2;
        if ( subshell_str == "M3") return Subshell::M3;
        if ( subshell_str == "M4") return Subshell::M4;
        if ( subshell_str == "M5") return Subshell::M5;
        if ( subshell_str == "N1") return Subshell::N1;
        if ( subshell_str == "N2") return Subshell::N2;
        if ( subshell_str == "N3") return Subshell::N3;
        if ( subshell_str == "N4") return Subshell::N4;
        if ( subshell_str == "N5") return Subshell::N5;
        if ( subshell_str == "N6") return Subshell::N6;
        if ( subshell_str == "N7") return Subshell::N7;
        if ( subshell_str == "O1") return Subshell::O1;
        if ( subshell_str == "O2") return Subshell::O2;
        if ( subshell_str == "O3") return Subshell::O3;
        if ( subshell_str == "O4") return Subshell::O4;
        if ( subshell_str == "O5") return Subshell::O5;
        if ( subshell_str == "O6") return Subshell::O6;
        if ( subshell_str == "O7") return Subshell::O7;
        if ( subshell_str == "P1") return Subshell::P1;
        if ( subshell_str == "P2") return Subshell::P2;
        if ( subshell_str == "P3") return Subshell::P3;
        if ( subshell_str == "P4") return Subshell::P4;
        if ( subshell_str == "P5") return Subshell::P5;
        if ( subshell_str == "Q1") return Subshell::Q1;
        if ( subshell_str == "Outer") return Subshell::OUTER;
}

std::string label(const Subshell subshell)
{
    switch (subshell)
    {
        case Subshell::K: return "K";
        case Subshell::L1: return "L1";
        case Subshell::L2: return "L2";
        case Subshell::L3: return "L3";
        case Subshell::M1: return "M1";
        case Subshell::M2: return "M2";
        case Subshell::M3: return "M3";
        case Subshell::M4: return "M4";
        case Subshell::M5: return "M5";
        case Subshell::N1: return "N1";
        case Subshell::N2: return "N2";
        case Subshell::N3: return "N3";
        case Subshell::N4: return "N4";
        case Subshell::N5: return "N5";
        case Subshell::N6: return "N6";
        case Subshell::N7: return "N7";
        case Subshell::O1: return "O1";
        case Subshell::O2: return "O2";
        case Subshell::O3: return "O3";
        case Subshell::O4: return "O4";
        case Subshell::O5: return "O5";
        case Subshell::O6: return "O6";
        case Subshell::O7: return "O7";
        case Subshell::P1: return "P1";
        case Subshell::P2: return "P2";
        case Subshell::P3: return "P3";
        case Subshell::P4: return "P4";
        case Subshell::P5: return "P5";
        case Subshell::Q1: return "Q1";
        case Subshell::OUTER: return "Outer";
    }
}

std::string orbital(const Subshell subshell)
{
    switch (subshell)
    {
        case Subshell::K: return "1s1/2";
        case Subshell::L1: return "2s1/2";
        case Subshell::L2: return "2p1/2";
        case Subshell::L3: return "2p3/2";
        case Subshell::M1: return "3s1/2";
        case Subshell::M2: return "3p1/2";
        case Subshell::M3: return "3p3/2";
        case Subshell::M4: return "3d3/2";
        case Subshell::M5: return "3d5/2";
        case Subshell::N1: return "4s1/2";
        case Subshell::N2: return "4p1/2";
        case Subshell::N3: return "4p3/2";
        case Subshell::N4: return "4d3/2";
        case Subshell::N5: return "4d5/2";
        case Subshell::N6: return "4f5/2";
        case Subshell::N7: return "4f7/2";
        case Subshell::O1: return "5s1/2";
        case Subshell::O2: return "5p1/2";
        case Subshell::O3: return "5p3/2";
        case Subshell::O4: return "5d3/2";
        case Subshell::O5: return "5d5/2";
        case Subshell::O6: return "5f5/2";
        case Subshell::O7: return "5f7/2";
        case Subshell::P1: return "6s1/2";
        case Subshell::P2: return "6p1/2";
        case Subshell::P3: return "6p3/2";
        case Subshell::P4: return "6d3/2";
        case Subshell::P5: return "6d5/2";
        case Subshell::Q1: return "7s1/2";
        case Subshell::OUTER: return "";
    }
}

std::ostream& operator << (std::ostream& stream, const Subshell subshell)
{
    stream << label(subshell);
    return stream;
}

bool isShellK(const Subshell subshell)
{
    if(subshell == Subshell::K)
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellL(const Subshell subshell)
{
    if(subshell == Subshell::L1 || subshell == Subshell::L2 || subshell == Subshell::L3)
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellM(const Subshell subshell)
{
    if(subshell == Subshell::M1 || subshell == Subshell::M2 || subshell == Subshell::M3 || subshell == Subshell::M4 || subshell == Subshell::M5 )
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellN(const Subshell subshell)
{
    if(subshell == Subshell::N1 || subshell == Subshell::N2 || subshell == Subshell::N3 || subshell == Subshell::N4 || subshell == Subshell::N5  || subshell == Subshell::N6 || subshell == Subshell::N7 )
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellO(const Subshell subshell)
{
    if(subshell == Subshell::O1 || subshell == Subshell::O2 || subshell == Subshell::O3 || subshell == Subshell::O4 || subshell == Subshell::O5  || subshell == Subshell::O6 || subshell == Subshell::O7 )
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellP(const Subshell subshell)
{
    if(subshell == Subshell::P1 || subshell == Subshell::P2 || subshell == Subshell::P3 || subshell == Subshell::P4 || subshell == Subshell::P5 )
    {
        return true;
    } else
    {
        return false;
    }
}

bool isShellQ(const Subshell subshell)
{
    if(subshell == Subshell::Q1)
    {
        return true;
    } else
    {
        return false;
    }
}
