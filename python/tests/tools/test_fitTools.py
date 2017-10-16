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
import xrayspectrumanalyzer.tools.fitTools as fitTools
import xrayspectrumanalyzer.tools.FitGaussianFunction as FitGaussianFunction

# Globals and constants variables.

class TestfitTools(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_FitObjectException(self):
        x = 10.2
        parameters = (1.0, 5.3, 86.3)
        fitObject = fitTools._FitObject()
        self.assertRaises(NotImplementedError, fitObject.evaluation, x, parameters)

        self.assertRaises(NotImplementedError, fitObject.getNumberFitParameters)

        #self.fail("Test if the testcase is working.")

    def test_FitFunctionsOneFunction(self):
        function = FitGaussianFunction.FitGaussianFunction()
        fitFunctions = fitTools.FitFunctions([function])
        self.assertEquals(3, fitFunctions.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000)
        fitFunctions = fitTools.FitFunctions([function])
        self.assertEquals(2, fitFunctions.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0)
        fitFunctions = fitTools.FitFunctions([function])
        self.assertEquals(1, fitFunctions.getNumberFitParameters())

        function = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0, sigma=1.5)
        fitFunctions = fitTools.FitFunctions([function])
        self.assertEquals(0, fitFunctions.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

    def test_FitFunctionsTwoFunction(self):
        function2 = FitGaussianFunction.FitGaussianFunction()

        function1 = FitGaussianFunction.FitGaussianFunction()
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(3+3, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(2+3, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(1+3, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0, sigma=1.5)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(0+3, fitFunctions.getNumberFitParameters())

        function2 = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0)

        function1 = FitGaussianFunction.FitGaussianFunction()
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(3+1, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(2+1, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(1+1, fitFunctions.getNumberFitParameters())

        function1 = FitGaussianFunction.FitGaussianFunction(area=1000, mu=2.0, sigma=1.5)
        fitFunctions = fitTools.FitFunctions([function1, function2])
        self.assertEquals(0+1, fitFunctions.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

# todo: add tests with fitting the Gaussian function.
# todo: add tests with fitting the FitFunctions class.

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.runmodule()
