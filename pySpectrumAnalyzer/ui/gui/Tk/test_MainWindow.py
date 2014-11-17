#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2937 $"
__svnDate__ = "$Date: 2014-09-01 10:20:37 -0400 (Mon, 01 Sep 2014) $"
__svnId__ = "$Id: test_MainWindow.py 2937 2014-09-01 14:20:37Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pySpectrumAnalyzer.ui.gui.Tk import MainWindow

# Globals and constants variables.

class TestMainWindow(unittest.TestCase):

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