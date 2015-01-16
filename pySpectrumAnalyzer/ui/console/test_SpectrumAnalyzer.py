#!/usr/bin/env python
"""
.. py:currentmodule:: pySpectrumAnalyzer.ui.console.test_SpectrumAnalyzer
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module `SpectrumAnalyzer`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "Dec 31, 2014"
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = "GPL 3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.

# Project modules
import pySpectrumAnalyzer.ui.console.SpectrumAnalyzer

# Globals and constants variables.

class TestSpectrumAnalyzer(unittest.TestCase):
    """
    TestCase class for the module `SpectrumAnalyzer`.
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

if __name__ == '__main__':  #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=pySpectrumAnalyzer.ui.console.SpectrumAnalyzer")
    nose.runmodule(argv=argv)
