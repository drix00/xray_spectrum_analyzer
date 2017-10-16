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
import unittest
import os.path

# Third party modules.
from nose import SkipTest

# Local modules.
from xrayspectrumanalyzer import get_current_module_path
import xrayspectrumanalyzer.tools.XRayTransitionData as XRayTransitionData

# Globals and constants variables.


class TestXRayTransitionData(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.xrayData = XRayTransitionData.XRayTransitionData()

        self.xrayData.readFiles()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadFiles(self):
        self.xrayData.readFiles()

        self.assertEquals(93, len(self.xrayData.lineData))

        self.assertEquals(2, len(self.xrayData.lineData[3]))

        self.assertEquals(54.3, self.xrayData.lineData[3]['Ka1']['energy_eV'])
        self.assertEquals(1.0, self.xrayData.lineData[3]['Ka1']['fraction'])

        self.assertEquals(54.3, self.xrayData.lineData[3]['Ka2']['energy_eV'])
        self.assertEquals(1.0, self.xrayData.lineData[3]['Ka2']['fraction'])

        self.assertEquals(93, len(self.xrayData.edgeData))

        self.assertEquals(1, len(self.xrayData.edgeData[3]))

        self.assertEquals(54.75, self.xrayData.edgeData[3]['K'])

        # self.fail("Test if the TestCase is working.")

    def testGetAtomicNumber(self):
        self.assertEquals(93, len(self.xrayData.getAtomicNumber()))

        self.assertEquals(93, len(self.xrayData.getAtomicNumber('both')))

        self.assertEquals(93, len(self.xrayData.getAtomicNumber('line')))

        self.assertEquals(93, len(self.xrayData.getAtomicNumber('edge')))

        # self.fail("Test if the TestCase is working.")

    def testGetSubshell(self):
        self.assertEquals(17, len(self.xrayData.getSubshell()))

        self.assertEquals(1, len(self.xrayData.getSubshell(6)))
        self.assertEquals(['K'], self.xrayData.getSubshell(6))

        self.assertEquals(4, len(self.xrayData.getSubshell([6, 13])))
        self.assertEquals(sorted(['K', 'LIII', 'LII', 'LI']), sorted(self.xrayData.getSubshell([6, 13])))

        self.assertEquals(13, len(self.xrayData.getSubshell([6, 13, 50])))

        # self.fail("Test if the TestCase is working.")

    def testGetIonizationEnergy_eV(self):
        self.assertEquals(283.79, self.xrayData.getIonizationEnergy_eV(6, 'K'))

        self.assertEquals(283.79, self.xrayData.getIonizationEnergy_eV(6, 'K'))

        self.assertEquals(82.8, self.xrayData.getIonizationEnergy_eV(79, 'NVII'))
        self.assertEquals(86.4, self.xrayData.getIonizationEnergy_eV(79, 'NVI'))
        self.assertEquals(107.8, self.xrayData.getIonizationEnergy_eV(79, 'OI'))
        self.assertEquals(333.89, self.xrayData.getIonizationEnergy_eV(79, 'NV'))
        self.assertEquals(351.99, self.xrayData.getIonizationEnergy_eV(79, 'NIV'))
        self.assertEquals(545.38, self.xrayData.getIonizationEnergy_eV(79, 'NIII'))
        self.assertEquals(643.67, self.xrayData.getIonizationEnergy_eV(79, 'NII'))
        self.assertEquals(758.77, self.xrayData.getIonizationEnergy_eV(79, 'NI'))
        self.assertEquals(2205.6, self.xrayData.getIonizationEnergy_eV(79, 'MV'))
        self.assertEquals(2291, self.xrayData.getIonizationEnergy_eV(79, 'MIV'))
        self.assertEquals(2742.9, self.xrayData.getIonizationEnergy_eV(79, 'MIII'))
        self.assertEquals(3147.7, self.xrayData.getIonizationEnergy_eV(79, 'MII'))
        self.assertEquals(3424.8, self.xrayData.getIonizationEnergy_eV(79, 'MI'))
        self.assertEquals(11918, self.xrayData.getIonizationEnergy_eV(79, 'LIII'))
        self.assertEquals(13733, self.xrayData.getIonizationEnergy_eV(79, 'LII'))
        self.assertEquals(14352, self.xrayData.getIonizationEnergy_eV(79, 'LI'))
        self.assertEquals(80722, self.xrayData.getIonizationEnergy_eV(79, 'K'))

        # self.fail("Test if the TestCase is working.")

    def testExtractSubshellKey(self):
        self.assertEquals('K', self.xrayData.extractSubshellKey('K1'))
        self.assertEquals('K', self.xrayData.extractSubshellKey('KI'))
        self.assertEquals('K', self.xrayData.extractSubshellKey('Kedge'))

        self.assertEquals('LI', self.xrayData.extractSubshellKey('L1'))
        self.assertEquals('LI', self.xrayData.extractSubshellKey('LI'))
        self.assertEquals('LI', self.xrayData.extractSubshellKey('LIEdge'))

        #        self.assertEquals(11918, self.xrayData.getIonizationEnergy_eV(79, 'LIIIedge'))
        #        self.assertEquals(13733, self.xrayData.getIonizationEnergy_eV(79, 'LIIedge'))
        #        self.assertEquals(14352, self.xrayData.getIonizationEnergy_eV(79, 'LIedge'))
        self.assertEquals('LIII', self.xrayData.extractSubshellKey('Ledge'))

        # self.fail("Test if the TestCase is working.")

    def testGetTransitionEnergy_eV(self):
        self.assertEquals(281.7700, self.xrayData.getTransitionEnergy_eV(6, 'Ka1'))
        self.assertEquals(281.7700, self.xrayData.getTransitionEnergy_eV(6, 'Ka2'))

        self.assertEquals(2117.9000, self.xrayData.getTransitionEnergy_eV(79, 'Ma2'))
        self.assertEquals(11914.0000, self.xrayData.getTransitionEnergy_eV(79, 'Lb5'))
        self.assertEquals(1980.8000, self.xrayData.getTransitionEnergy_eV(79, 'M3N1'))

        self.assertEquals(4510.0, self.xrayData.getTransitionEnergy_eV("Ti", 'Ka'))
        self.assertEquals(4950.9, self.xrayData.getTransitionEnergy_eV("V", 'Ka'))

        # self.fail("Test if the TestCase is working.")

    def testGetTransitionFraction(self):
        self.assertEquals(1.00000, self.xrayData.getTransitionFraction(6, 'Ka1'))
        self.assertEquals(0.50000, self.xrayData.getTransitionFraction(6, 'Ka2'))

        self.assertEquals(1.00000, self.xrayData.getTransitionFraction(79, 'Ma2'))
        self.assertEquals(1.00000, self.xrayData.getTransitionFraction(79, 'Ma1'))
        self.assertEquals(1.00000, self.xrayData.getTransitionFraction(79, 'La1'))
        self.assertEquals(1.00000, self.xrayData.getTransitionFraction(79, 'Ka1'))
        self.assertEquals(0.59443, self.xrayData.getTransitionFraction(79, 'Mb'))
        self.assertEquals(0.50000, self.xrayData.getTransitionFraction(79, 'Ka2'))
        self.assertEquals(0.40151, self.xrayData.getTransitionFraction(79, 'Lb1'))
        self.assertEquals(0.21949, self.xrayData.getTransitionFraction(79, 'Lb2'))
        self.assertEquals(0.15000, self.xrayData.getTransitionFraction(79, 'Kb3'))
        self.assertEquals(0.15000, self.xrayData.getTransitionFraction(79, 'Kb1'))
        self.assertEquals(0.11390, self.xrayData.getTransitionFraction(79, 'La2'))
        self.assertEquals(0.08505, self.xrayData.getTransitionFraction(79, 'Mg'))
        self.assertEquals(0.08407, self.xrayData.getTransitionFraction(79, 'Lg1'))
        self.assertEquals(0.06900, self.xrayData.getTransitionFraction(79, 'Lb3'))
        self.assertEquals(0.05940, self.xrayData.getTransitionFraction(79, 'Lb4'))
        self.assertEquals(0.05620, self.xrayData.getTransitionFraction(79, 'Ll'))
        self.assertEquals(0.05000, self.xrayData.getTransitionFraction(79, 'Kb2'))
        self.assertEquals(0.04511, self.xrayData.getTransitionFraction(79, 'Mz2'))
        self.assertEquals(0.04380, self.xrayData.getTransitionFraction(79, 'Lb5'))
        self.assertEquals(0.02901, self.xrayData.getTransitionFraction(79, 'M3N1'))

        # self.fail("Test if the TestCase is working.")

    def testConfigurationFile(self):
        xrayData = XRayTransitionData.XRayTransitionData()

        self.assertEquals('XrayDataLine.csv', xrayData.lineFilename)
        self.assertEquals('XrayDataEdge.csv', xrayData.edgeFilename)

        # self.fail("Test if the TestCase is working.")

    def testGetSubshellEnergyRange(self):
        transitionsEnergies_eV = self.xrayData.getSubshellEnergies(atomicNumber=79
                                                                   , subshell='K'
                                                                   , restricted=True)
        self.assertEqual(len(transitionsEnergies_eV.keys()), 4)
        self.assertEqual(transitionsEnergies_eV['Ka1'], 68816.0)

        transitionsEnergies_eV = self.xrayData.getSubshellEnergies(atomicNumber=79
                                                                   , subshell='LIII'
                                                                   , restricted=True)
        self.assertEqual(len(transitionsEnergies_eV.keys()), 5)
        self.assertEqual(transitionsEnergies_eV['La1'], 9711.8)

        transitionsEnergies_eV = self.xrayData.getSubshellEnergies(atomicNumber=79
                                                                   , subshell='MV'
                                                                   , restricted=True)
        self.assertEqual(len(transitionsEnergies_eV.keys()), 3)
        self.assertEqual(transitionsEnergies_eV['Ma1'], 2121.8)


if __name__ == '__main__':  # pragma: no cover
    import nose
    nose.runmodule()
