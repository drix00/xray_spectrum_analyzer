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
import warnings
import csv

# Third party modules.

# Local modules.
import pywinxraydata.XRayDataWinxray as XRayDataWinxray
import pywinxraydata.ElementProperties as ElementProperties
from xrayspectrumanalyzer import get_current_module_path

# Globals and constants variables.

class XRayTransitionData(object):
    def __init__(self):

        self.lineFilename = "XrayDataLine.csv"

        self.edgeFilename = "XrayDataEdge.csv"

        self.readFiles()

        self.restrictedXRayLines = ['Ka1', 'Ka2', 'Kb1', 'Kb3'
            , 'La1', 'La2', 'Lb2', 'Ll'
            , 'Lb1', 'Le'
            , 'Ma1', 'Mz1'
            , 'Mb1', 'Mz2']

        self.restrictedXRayLines2 = ['Ka1', 'Ka2', 'Kb1', 'Kb3'
            , 'La1', 'La2', 'Lb2', 'Lb5', 'Lb15', 'Ll'
            , 'Lb1', 'Lg1', 'Le'
            , 'Lb3', 'Lb4', 'Lg2', 'Lg3'
            , 'Ma1', 'Ma2', 'Mz1'
            , 'Mb1', 'Mz2', 'Mg1'
            , 'Md']

    def readLineFile(self, filename):
        # pylint: disable-msg=W0201
        reader = csv.reader(open(filename, 'r'))

        # Extract header
        row = next(reader)

        keys = []
        for value in row:
            if value[0] == '#':
                value = value[1:]

            value = value.strip()
            value = value.replace(' ', '_')
            value = value.replace('(', '')
            value = value.replace(')', '')

            keys.append(value)

        self.lineData = {}

        for row in reader:
            try:
                atomicNumber = int(row[0])
                energy_eV = float(row[1])
                fraction = float(row[2])
                line = row[3]

                self.lineData.setdefault(atomicNumber, {})

                self.lineData[atomicNumber].setdefault(line, {})

                self.lineData[atomicNumber][line]['energy_eV'] = energy_eV
                self.lineData[atomicNumber][line]['fraction'] = fraction

            except ValueError:
                print(row)

    def readEdgeFile(self, filename):
        # pylint: disable-msg=W0201
        reader = csv.reader(open(filename, 'r'))

        # Extract header
        row = next(reader)

        keys = []
        for value in row:
            if value[0] == '#':
                value = value[1:]

            value = value.strip()
            value = value.replace(' ', '_')
            value = value.replace('(', '')
            value = value.replace(')', '')

            keys.append(value)

        self.edgeData = {}

        for row in reader:
            try:
                atomicNumber = int(row[0])
                energy_eV = float(row[1])
                subshell = row[2]

                subshell = subshell.replace('edge', '')

                if len(subshell) > 4:
                    print(atomicNumber, subshell)

                self.edgeData.setdefault(atomicNumber, {})

                self.edgeData[atomicNumber].setdefault(subshell, energy_eV)
            except ValueError:
                print(row)

    def readFiles(self):
        data_path = get_current_module_path(__file__, "../../../data/")
        completeFilename = os.path.join(data_path, self.lineFilename)
        self.readLineFile(completeFilename)

        completeFilename = os.path.join(data_path, self.edgeFilename)
        self.readEdgeFile(completeFilename)

    def getAtomicNumber(self, dataType='both'):
        if dataType == 'both':
            atomicNumbers = self.lineData.keys()

            for atomicNumber in self.edgeData:
                if not atomicNumber in atomicNumbers:
                    atomicNumbers.append(atomicNumber)
        elif dataType == 'line':
            atomicNumbers = self.lineData.keys()
        elif dataType == 'edge':
            atomicNumbers = self.edgeData.keys()
        else:
            raise AttributeError(dataType)

        return atomicNumbers

    def getSubshellFromEnergy(self, atomicNumber, energy_eV, limit_eV=100.0):
        subshells = self.getSubshell(atomicNumber)

        if atomicNumber == 92:
            limit_eV = 500

        for subshell in subshells:
            subshellEnergy_eV = self.getIonizationEnergy_eV(atomicNumber, subshell)

            if energy_eV > (subshellEnergy_eV - limit_eV) and energy_eV < (subshellEnergy_eV + limit_eV):
                return subshell

    def getSubshell(self, atomicNumbers=None):
        subshells = []

        if not atomicNumbers:
            for atomicNumber in self.edgeData:
                for subshell in self.edgeData[atomicNumber]:
                    if not subshell in subshells:
                        subshells.append(subshell)
        elif type(atomicNumbers) is type(list()):
            for atomicNumber in atomicNumbers:
                if atomicNumber in self.edgeData:
                    for subshell in self.edgeData[atomicNumber]:
                        if not subshell in subshells:
                            subshells.append(subshell)
        else:
            atomicNumber = atomicNumbers
            if atomicNumber in self.edgeData:
                for subshell in self.edgeData[atomicNumber]:
                    if not subshell in subshells:
                        subshells.append(subshell)

        return subshells

    def getTransitionFromEnergy(self, atomicNumber, energy_eV, limit_eV=10.0):
        transitions = self.getTransition(atomicNumber)

        for transitionName in transitions:
            lineEnergy_eV = self.getTransitionEnergy_eV(atomicNumber, transitionName)

            if energy_eV > (lineEnergy_eV - limit_eV) and energy_eV < (lineEnergy_eV + limit_eV):
                return transitionName

    def getTransition(self, atomicNumbers=None, restricted=False):
        transitions = []

        if not atomicNumbers:
            for atomicNumber in self.lineData:
                for transition in self.lineData[atomicNumber]:
                    if not transition in transitions:
                        if not restricted:
                            transitions.append(transition)
                        elif transition in self.restrictedXRayLines:
                            transitions.append(transition)

        elif type(atomicNumbers) is type(list()):
            for atomicNumber in atomicNumbers:
                if atomicNumber in self.lineData:
                    for transition in self.lineData[atomicNumber]:
                        if not transition in transitions:
                            if not restricted:
                                transitions.append(transition)
                            elif transition in self.restrictedXRayLines:
                                transitions.append(transition)
        else:
            atomicNumber = atomicNumbers
            if atomicNumber in self.lineData:
                for transition in self.lineData[atomicNumber]:
                    if not transition in transitions:
                        if not restricted:
                            transitions.append(transition)
                        elif transition in self.restrictedXRayLines:
                            transitions.append(transition)

        transitions.sort()

        return transitions

    def extractSubshellKey(self, subshell):
        # O shell
        if subshell[0].upper() == 'O':
            return 'OI'

        # N shell
        if 'N7' in subshell.upper() or 'NVII' in subshell.upper():
            return 'NVII'

        if 'N6' in subshell.upper() or 'NVI' in subshell.upper():
            return 'NVI'

        if 'N5' in subshell.upper() or 'NV' in subshell.upper():
            return 'NV'

        if 'N4' in subshell.upper() or 'NIV' in subshell.upper():
            return 'NIV'

        if 'N3' in subshell.upper() or 'NIII' in subshell.upper():
            return 'NIII'

        if 'N2' in subshell.upper() or 'NII' in subshell.upper():
            return 'NII'

        if 'N1' in subshell.upper() or 'NI' in subshell.upper():
            return 'NI'

        if subshell[0].upper() == 'N':
            return 'NV'

        # M shell
        if 'M5' in subshell.upper() or 'MV' in subshell.upper():
            return 'MV'

        if 'M4' in subshell.upper() or 'MIV' in subshell.upper():
            return 'MIV'

        if 'M3' in subshell.upper() or 'MIII' in subshell.upper():
            return 'MIII'

        if 'M2' in subshell.upper() or 'MII' in subshell.upper():
            return 'MII'

        if 'M1' in subshell.upper() or 'MI' in subshell.upper():
            return 'MI'

        if subshell[0].upper() == 'M':
            return 'MV'

        # L shell
        if 'L3' in subshell.upper() or 'LIII' in subshell.upper():
            return 'LIII'

        if 'L2' in subshell.upper() or 'LII' in subshell.upper():
            return 'LII'

        if 'L1' in subshell.upper() or 'LI' in subshell.upper():
            return 'LI'

        if subshell[0].upper() == 'L':
            return 'LIII'

        # K shell
        if subshell[0].upper() == 'K':
            return 'K'

        print(subshell)
        return subshell

    def getIonizationEnergy_eV(self, element, subshell):
        if isinstance(element, int):
            atomicNumber = element
        elif isinstance(element, str):
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(element)

        return self._getIonizationEnergy_eV(atomicNumber, subshell)

    def _getIonizationEnergy_eV(self, atomicNumber, subshell):

        subshellKey = self.extractSubshellKey(subshell)

        if atomicNumber in self.edgeData and subshellKey in self.edgeData[atomicNumber]:
            return self.edgeData[atomicNumber][subshellKey]
        else:
            message = "Using x-ray data from winxray for %s subshell of %i" % (subshell, atomicNumber)
            warnings.warn(message)

            return XRayDataWinxray.getIonizationEnergy_eV(atomicNumber, subshell)

    def extractTransitionKey(self, atomicNumber, transitionName):

        transitions = self.getTransition(atomicNumber)

        transitions.sort()

        for transition in transitions:
            if transitionName in transition:
                return transition

        return transitionName

    def getTransitionEnergy_eV(self, element, transitionName):
        if isinstance(element, int):
            atomicNumber = element
        elif isinstance(element, str):
            atomicNumber = ElementProperties.getAtomicNumberBySymbol(element)

        return self._getTransitionEnergy_eV(atomicNumber, transitionName)

    def _getTransitionEnergy_eV(self, atomicNumber, transitionName):
        if atomicNumber in self.lineData:
            transitionKey = self.extractTransitionKey(atomicNumber, transitionName)

            if transitionKey in self.lineData[atomicNumber]:
                return self.lineData[atomicNumber][transitionKey]['energy_eV']

        message = "No data for the atomic number %i" % (atomicNumber)
        warnings.warn(message)

        return 0.0

    def getTransitionFraction(self, atomicNumber, transitionName):

        transitionKey = self.extractTransitionKey(atomicNumber, transitionName)

        return self.lineData[atomicNumber][transitionKey]['fraction']

    def getSubshellEnergies(self, atomicNumber, subshell, restricted=True):
        """
        Return a dictionary with all the transitions and energies for a given *subshell*.

        :arg atomicNumber: atomic number of the element
        :type atomicNumber: :keyword:`int`

        :arg subshell: subshell symbol
        :type subshell: :keyword:`str`

        :arg restricted: ?
        :type restricted: :keyword:`bool`

        :rtype: :keyword:`dict`
        """
        transitions = self.getTransition(atomicNumbers=[atomicNumber], restricted=restricted)

        transtitionsEnergies_eV = {}
        for transition in transitions:
            if self.extractSubshellKey(transition) == subshell.upper():
                transitionEnergy_eV = self.getTransitionEnergy_eV(element=atomicNumber
                                                                  , transitionName=transition)
                transtitionsEnergies_eV.setdefault(transition, transitionEnergy_eV)

        return transtitionsEnergies_eV
