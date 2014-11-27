#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2378 $"
__svnDate__ = "$Date: 2011-06-20 15:45:48 -0400 (Mon, 20 Jun 2011) $"
__svnId__ = "$Id: test_SpectrumAnalyzerGUI.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import pySpectrumAnalyzer.SpectrumAnalyzerGUI as SpectrumAnalyzerGUI

# Globals and constants variables.

class TestSpectrumAnalyzerGUI(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from pyHendrixDemersTools.Testings import runTestModule
    runTestModule()
