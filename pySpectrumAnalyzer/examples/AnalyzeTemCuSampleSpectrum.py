#!/usr/bin/env python
""" """

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
import os.path

# Third party modules.
import pylab
import numpy as np

# Local modules.
import pyHendrixDemersTools.Files as Files
import pyHendrixDemersTools.Graphics as Graphics
import pySpectrumAnalyzer.tools.XRayTransitionData as XRayTransitionData

import pySpectrumFileFormat.Edax.TemCsvFile as TemCsvFile

# Globals and constants variables.
ENERGIES_eV = "Energies_eV"
COUNTS = "Counts"

class AnalyzeTemCuSampleSpectrum(object):
    def __init__(self, output):
        self._initParameters()

        self._output = output

        configurationFile = Files.getCurrentModulePath(__file__, "AnalyzeTemCuSampleSpectrum.cfg")
        self._path = Files.getCnseResultsPath(configurationFile, "TEM/Hamed/EDS")

        self._xRayTransitionData = XRayTransitionData.XRayTransitionData(configurationFile)

        # OVERALL.CSV and SMALL.CSV are the same files.
        self._filenames = ["OVERALL.CSV", "SMALL2.CSV"]

    def _initParameters(self):
        self._energyMin_eV = 1390.0
        self._energyMax_eV = 3000.0
        self._sulfurColor = 'r'
        self._platinumColor = 'g'

    def readFiles(self):
        data = {}

        for filename in self._filenames:
            data.setdefault(filename, {})
            filepath = os.path.join(self._path, filename)

            energies_eV, counts = TemCsvFile.TemCsvFile(filepath).getData()
            data[filename][ENERGIES_eV] = energies_eV
            data[filename][COUNTS] = counts

        self._data = data

    def createGraphics(self):
        self._createAllSpectrumGraphics()
        self._createCompareSpectrumGraphics()
        self._createAllSpectrumPtM_SKGraphics()

    def _createAllSpectrumGraphics(self):
        for filename in self._filenames:
            self._createSpectrumGraphic(filename)

    def _createSpectrumGraphic(self, filename):
        pylab.figure()

        energies_eV = self.getEnergies_eV(filename)
        counts = self.getCounts(filename)

        pylab.plot(energies_eV, counts)

        pylab.title(filename)

        pylab.xlabel("Energy (eV)")
        pylab.ylabel("Counts")

    def getEnergies_eV(self, filename):
            energies_eV = self._data[filename][ENERGIES_eV]
            return energies_eV

    def getCounts(self, filename):
            counts = self._data[filename][COUNTS]
            return counts

    def _createCompareSpectrumGraphics(self):
        pylab.figure()

        for filename in self._filenames:
            energies_eV = self.getEnergies_eV(filename)
            countsNormalized = self.getCountsNormalized(filename)

            label = filename
            pylab.plot(energies_eV, countsNormalized, label=label)

        pylab.xlabel("Energy (eV)")
        pylab.ylabel("Counts Normalized")
        pylab.legend(loc='best')

    def getCountsNormalized(self, filename):
            counts = np.array(self.getCounts(filename))
            total = float(sum(counts))
            countsNormalized = counts / total
            return countsNormalized

    def _createAllSpectrumPtM_SKGraphics(self):
        for filename in self._filenames:
            self._createSpectrumPtM_SKGraphic(filename)

    def _createSpectrumPtM_SKGraphic(self, filename):
        pylab.figure()

        energies_eV, counts = self.getPtMandSK_Data(filename)

        pylab.plot(energies_eV, counts)

        self._drawTransitionsSulfurK(energies_eV, counts)

        self._drawTransitionsPlatinumM(energies_eV, counts)

        pylab.title(filename)

        pylab.xlabel("Energy (eV)")
        pylab.ylabel("Counts")

    def getPtMandSK_Data(self, filename):
        energies_eV = np.array(self.getEnergies_eV(filename))
        counts = np.array(self.getCounts(filename))

        mask = np.all([energies_eV > self._energyMin_eV, energies_eV < self._energyMax_eV], axis=0)

        energies_eV = energies_eV[mask]
        counts = counts[mask]

        return energies_eV, counts

    def _drawTransitionsSulfurK(self, energies_eV, counts):
            transitionInfo = self._getTransitionInfoSulfurK()

            self._drawTransitions(transitionInfo, "Ka", energies_eV, counts, self._sulfurColor)

    def _getTransitionInfoSulfurK(self):
        atomicNumber = 16

        return self._getTransitionInfo(atomicNumber, 'K')

    def _getTransitionInfo(self, atomicNumber, majorLine):
        transitions = self._xRayTransitionData.getTransition(atomicNumber)

        transitionsLine = []
        for transition in transitions:
            if transition[0] == majorLine:
                transitionsLine.append(transition)

        transitionInfo = {}

        for transition in transitionsLine:
            energy_eV = self._xRayTransitionData.getTransitionEnergy_eV(atomicNumber, transition)
            fraction = self._xRayTransitionData.getTransitionFraction(atomicNumber, transition)

            transitionInfo[transition] = (energy_eV, fraction)

        return transitionInfo

    def _drawTransitions(self, transitionInfo, line, energies_eV, counts, color):
            numberLine = 0
            mainLineEnergy_eV = 0.0
            mainLineFraction = 0.0
            for transition in transitionInfo:
                    if transition[:2] == line:
                            mainLineEnergy_eV += transitionInfo[transition][0]
                            numberLine += 1
                            mainLineFraction += transitionInfo[transition][1]

            mainLineEnergy_eV /= numberLine
            step_eV = 10.0 / 2
            mask = np.all([energies_eV > mainLineEnergy_eV - step_eV, energies_eV < mainLineEnergy_eV + step_eV], axis=0)
            mainLineCount = sum(counts[mask])
            print(mainLineEnergy_eV, mainLineFraction, mainLineCount)
            for transition in transitionInfo:
                    energy_eV, fraction = transitionInfo[transition]
                    ymax = pylab.ylim()[1]
                    ymax = (mainLineCount * fraction) / ymax
                    pylab.axvline(x=energy_eV, ymax=fraction, color=color)

    def _getTransitionInfoPlatinumM(self):
        atomicNumber = 78

        return self._getTransitionInfo(atomicNumber, 'M')

    def _drawTransitionsPlatinumM(self, energies_eV, counts):
            transitionInfo = self._getTransitionInfoPlatinumM()

            self._drawTransitions(transitionInfo, "Ma", energies_eV, counts, self._platinumColor)

def run():
    output = Graphics.DISPLAY
    #Graphics.setDefault(output)

    analyze = AnalyzeTemCuSampleSpectrum(output)
    analyze.readFiles()

    analyze.createGraphics()

    if output == Graphics.DISPLAY:
        pylab.show()

if __name__ == '__main__':    #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
