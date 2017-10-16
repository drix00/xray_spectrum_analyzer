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
import logging

# Third party modules.

# Local modules.
import xrayspectrumanalyzer.tools.ElementProperties as ElementProperties

# Globals and constants variables.

class TestElementProperties(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetMassDensity_g_cm3(self):
        self.assertEquals(7.1900, ElementProperties.getMassDensity_g_cm3(24))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetAtomicMass_g_mol(self):
        self.assertEquals(51.996000, ElementProperties.getAtomicMass_g_mol(24))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetFermiEnergy_eV(self):
        self.assertEquals(1.000, ElementProperties.getFermiEnergy_eV(24))

        self.assertEquals(4.700, ElementProperties.getFermiEnergy_eV(3))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetKFermi_eV(self):
        self.assertEquals(7.00E7, ElementProperties.getKFermi_eV(24))

        self.assertEquals(1.10E8, ElementProperties.getKFermi_eV(3))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetPlasmonEnergy_eV(self):
        self.assertEquals(24.9, ElementProperties.getPlasmonEnergy_eV(24))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeAtomicDensity_atom_cm3(self):
        massDensity_g_cm3 = ElementProperties.getMassDensity_g_cm3(13)
        atomicMass_g_mol = ElementProperties.getAtomicMass_g_mol(13)

        value = ElementProperties.computeAtomicDensity_atom_cm3(massDensity_g_cm3, atomicMass_g_mol)
        value *= 1.0E-22

        self.assertAlmostEquals(6.02617011482666, value, 4)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetKRatioCorrection(self):
        self.assertAlmostEquals(0.80707, ElementProperties.getKRatioCorrection(13), 4)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetMeanIonizationEnergy_eV(self):
        self.assertEquals(149.5, ElementProperties.getMeanIonizationEnergy_eV(13))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetSymbol(self):
        self.assertEquals('Al', ElementProperties.getSymbol(13))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetName(self):
        self.assertEquals('Aluminium', ElementProperties.getName(13))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
