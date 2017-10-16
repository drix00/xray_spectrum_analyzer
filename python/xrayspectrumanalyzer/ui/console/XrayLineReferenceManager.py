#!/usr/bin/env python
"""
.. py:currentmodule:: console.XrayLineReferenceManager
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

X-ray lines reference manager
"""

###############################################################################
# Copyright 2016 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.

# Third party modules.

# Local modules.
import xrayspectrumanalyzer.tools.XRayTransitionData as XRayTransitionData
import xrayspectrumanalyzer.tools.ElementProperties as ElementProperties

# Project modules

# Globals and constants variables.
FRACTION_MINOR_MAJOR = 0.05

class XrayLineReferenceManager(object):
    def __init__(self):
        self._xrayData = XRayTransitionData.XRayTransitionData()
        self._xrayData.readFiles()

        self._elementSymbols = []

    def addElement(self, symbol):
        self._elementSymbols.append(symbol)

    def getAbsorptionEdges(self):
        absorptionEdges = []

        for symbol in self._elementSymbols:
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            shells = self._xrayData.getSubshell(atomicNumber)
            for shell in shells:
                position_eV = self._xrayData.getIonizationEnergy_eV(atomicNumber, shell)
                position_keV = position_eV/1.0e3
                label = "%s %s" % (symbol, shell)
                absorptionEdges.append((position_keV, label))

        return absorptionEdges

    def getMajorLines(self):
        majorLines = []

        for symbol in self._elementSymbols:
            positions_keV = set()
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            transitions = self._xrayData.getTransition(atomicNumber, restricted=False)
            for transition in transitions:
                position_eV = self._xrayData.getTransitionEnergy_eV(atomicNumber, transition)
                fraction = self._xrayData.getTransitionFraction(atomicNumber, transition)
                position_keV = position_eV/1.0e3
                label = "%s %s" % (symbol, transition)
                if (fraction > FRACTION_MINOR_MAJOR and self.notSamePosition_keV(position_keV, positions_keV)):
                    majorLines.append((position_keV, fraction, label))
                    positions_keV.add(position_keV)

        return majorLines

    def notSamePosition_keV(self, position_keV, positions_keV):
        for positionRef_keV in positions_keV:
            if abs(position_keV - positionRef_keV) < 0.01:
                return False

        return True

    def getLines(self, peaks):
        lines = []

        for peak in peaks:
            symbol, peakLabel = peak
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            transitions = self._xrayData.getTransition(atomicNumber, restricted=False)

            transition = peakLabel
            if transition in transitions:
                position_eV = self._xrayData.getTransitionEnergy_eV(atomicNumber, transition)
                fraction = self._xrayData.getTransitionFraction(atomicNumber, transition)
                position_keV = position_eV/1.0e3
                label = "%s %s" % (symbol, transition)
                lines.append((position_keV, fraction, label))

        return lines

    def getMinorLines(self):
        minorLines = []

        for symbol in self._elementSymbols:
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            transitions = self._xrayData.getTransition(atomicNumber, restricted=False)
            for transition in transitions:
                position_eV = self._xrayData.getTransitionEnergy_eV(atomicNumber, transition)
                fraction = self._xrayData.getTransitionFraction(atomicNumber, transition)
                position_keV = position_eV/1.0e3
                label = "%s %s" % (symbol, transition)
                if (fraction <= FRACTION_MINOR_MAJOR):
                    minorLines.append((position_keV, fraction, label))

        return minorLines

    def getSatelliteLines(self):
        satelliteLines = []
        for symbol in self._elementSymbols:
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            transitions = self._xrayData.getTransition(atomicNumber, restricted=False)
            for transition in transitions:
                if transition.startswith('S') or 'satellite' in transition:
                    position_eV = self._xrayData.getTransitionEnergy_eV(atomicNumber, transition)
                    fraction = self._xrayData.getTransitionFraction(atomicNumber, transition)
                    position_keV = position_eV/1.0e3
                    label = "%s %s" % (symbol, transition)
                    satelliteLines.append((position_keV, fraction, label))

        return satelliteLines

    def getSiEscapePeaks(self):
        siKaLineEnergy_keV = self._xrayData.getTransitionEnergy_eV(14, 'Ka1')/1.0e3

        escapePeaks = []
        for symbol in self._elementSymbols:
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(symbol)
            transitions = self._xrayData.getTransition(atomicNumber, restricted=False)
            for transition in transitions:
                position_eV = self._xrayData.getTransitionEnergy_eV(atomicNumber, transition)
                fraction = self._xrayData.getTransitionFraction(atomicNumber, transition)
                position_keV = position_eV/1.0e3 - siKaLineEnergy_keV
                label = "E %s %s - Si Ka" % (symbol, transition)
                if (position_keV > siKaLineEnergy_keV and fraction > FRACTION_MINOR_MAJOR):
                    escapePeaks.append((position_keV, label))

        return escapePeaks
