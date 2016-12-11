#!/usr/bin/env python
"""
.. py:currentmodule:: ProbeBroadening3D.fit.FitPolynomialFunction
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

description
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
import pySpectrumAnalyzer.tools.FitPolynomialFunction as FitPolynomialFunction

# Globals and constants variables.

class TestFitPolynomialFunction(unittest.TestCase):
    """
    TestCase class for the module `FitPolynomialFunction`.
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

    def test_FitPolynomialFirstDegreeFunction(self):
        function = FitPolynomialFunction.FitPolynomialFirstDegreeFunction()
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialFirstDegreeFunction(a=1000)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialFirstDegreeFunction(a=1000, b=2.0)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

    def test_FitPolynomialSecondDegreeFunction(self):
        function = FitPolynomialFunction.FitPolynomialSecondDegreeFunction()
        self.assertEquals(3, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialSecondDegreeFunction(a=1000)
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialSecondDegreeFunction(a=1000, b=2.0)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialSecondDegreeFunction(a=1000, b=2.0, c=9.0)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

    def test_FitPolynomialThirdDegreeFunction(self):
        function = FitPolynomialFunction.FitPolynomialThirdDegreeFunction()
        self.assertEquals(4, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialThirdDegreeFunction(a=1000)
        self.assertEquals(3, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialThirdDegreeFunction(a=1000, b=2.0)
        self.assertEquals(2, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialThirdDegreeFunction(a=1000, b=2.0, c=9.0)
        self.assertEquals(1, function.getNumberFitParameters())

        function = FitPolynomialFunction.FitPolynomialThirdDegreeFunction(a=1000, b=2.0, c=9.0, d=56.9)
        self.assertEquals(0, function.getNumberFitParameters())

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.runmodule()
