#!/usr/bin/env python
"""
.. py:currentmodule:: console.test_FitLine
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for module `FitLine`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

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
