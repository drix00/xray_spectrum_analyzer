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

# Project modules
import xrayspectrumanalyzer.tools.FitGaussianFunction as FitGaussianFunction

# Globals and constants variables.

class TestFitGaussianFunction(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_FitGaussianFunction(self):
        function = FitGaussianFunction.FitGaussianFunction()
        self.assertEquals(3, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000)
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0, sigma=1.5)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

    def test_FitGaussianWithYFunction(self):
        function = FitGaussianFunction.FitGaussianWithYFunction()
        self.assertEquals(4, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianWithYFunction(area=1000)
        self.assertEquals(3, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianWithYFunction(area=1000, mu=2.0)
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianWithYFunction(area=1000, mu=2.0, sigma=1.5)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianWithYFunction(area=1000, mu=2.0, sigma=1.5, y0=5.7)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.runmodule()
