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
__svnId__ = "$Id: test_Spectrum.py 2378 2011-06-20 19:45:48Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import Spectrum
import DrixUtilities.Files as Files

# Globals and constants variables.

class TestSpectrum(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.spectrum = Spectrum.Spectrum()

        self.filename = Files.getCurrentModulePath(__file__, "inputData/Spectrum 2.txt")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadFile(self):
        self.spectrum.readFile(self.filename)

        self.assertEquals(self.filename, self.spectrum.filename)

        self.assertAlmostEquals(10.0, self.spectrum.emsa.getBeamEnergy(), 1)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModule
    runTestModule()
