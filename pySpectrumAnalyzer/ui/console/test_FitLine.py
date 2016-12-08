#!/usr/bin/env python
"""
.. py:currentmodule:: console.test_FitLine
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for module `FitLine`.
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
import unittest
import logging

# Third party modules.

# Local modules.

# Project modules
import pySpectrumAnalyzer.ui.console.FitLine as FitLine

# Globals and constants variables.

class TestFitLine(unittest.TestCase):
    """
    TestCase class for the module `FitLine`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_FitGaussianFunction(self):
        function = FitLine.FitLineKa1Ka2()
        self.assertEquals(5, function.getNumberFitParameters())

        function = FitLine.FitLineKa1Ka2(areaKa1=1000)
        self.assertEquals(4, function.getNumberFitParameters())

        function = FitLine.FitLineKa1Ka2(areaKa1=1000, fractionKa2=0.5)
        self.assertEquals(3, function.getNumberFitParameters())

        function = FitLine.FitLineKa1Ka2(areaKa1=1000, fractionKa2=0.5, muKa1=1.2)
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitLine.FitLineKa1Ka2(areaKa1=1000, fractionKa2=0.5, muKa1=1.2, differenceKa2=0.001)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitLine.FitLineKa1Ka2(areaKa1=1000, fractionKa2=0.5, muKa1=1.2, differenceKa2=0.001, sigmaKa=0.050)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=pySpectrumAnalyzer.ui.console.FitLine")
    nose.runmodule(argv=argv)
