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

# Third party modules.

# Local modules.
import xrayspectrumanalyzer.tools.XRayDataWinxray as XRayDataWinxray

# Globals and constants variables.

class TestXRayDataWinxray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetXRayEnergy_eV(self):
        self.assertAlmostEquals(282.0, XRayDataWinxray.getXRayEnergy_eV(6, 'Ka1'))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetIonizationEnergy_eV(self):
        self.assertAlmostEquals(283.0, XRayDataWinxray.getIonizationEnergy_eV(6, 'K'))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
