#!/usr/bin/env python
"""
.. py:currentmodule:: xrayspectrumanalyzer.ui.console.test_XrayLineReferenceManager
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module `XrayLineReferenceManager`.
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
import pySpectrumAnalyzer.ui.console.XrayLineReferenceManager

# Globals and constants variables.

class TestXrayLineReferenceManager(unittest.TestCase):
    """
    TestCase class for the module `XrayLineReferenceManager`.
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
    argv.append("--cover-package=xrayspectrumanalyzer.ui.console.XrayLineReferenceManager")
    nose.runmodule(argv=argv)
