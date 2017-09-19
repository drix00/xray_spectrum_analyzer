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
import pySpectrumAnalyzer.ui.gui.Tk.SpectrumAnalyzerData as SpectrumAnalyzerData

# Globals and constants variables.

class TestSpectrumAnalyzerData(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__': #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=xrayspectrumanalyzer.ui.gui.Tk.SpectrumAnalyzerData")
    nose.runmodule(argv=argv)
