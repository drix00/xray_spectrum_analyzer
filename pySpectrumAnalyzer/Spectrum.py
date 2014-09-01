#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2600 $"
__svnDate__ = "$Date: 2011-11-22 23:48:41 -0500 (Tue, 22 Nov 2011) $"
__svnId__ = "$Id: Spectrum.py 2600 2011-11-23 04:48:41Z hdemers $"

# Standard library modules.
import os.path

# Third party modules.
import pylab

# Local modules.
import SpectrumFileFormatTools.emmff.emsaFormat as emsaFormat
import DuaneHuntLimit.myklebust1990 as DuaneHuntLimit

# Globals and constants variables.

class Spectrum(object):
    def __init__(self, filename=None):
        self.duaneHuntLimit = None

        if filename:
            self.readFile(filename)

    def readFile(self, filename):
        # pylint: disable-msg=W0201
        self.emsa = emsaFormat.EmsaFormat(filename)
        self.filename = filename

    def computeDuaneHuntLimit(self):
        manager = DuaneHuntLimit.FitManager()
        manager.readEMSAFile(self.filename)

        manager.fit()

        self.duaneHuntLimit = manager.getDuaneHuntLimit()

        print self.duaneHuntLimit

    def show(self, plotCommand=pylab.plot):
        if self.emsa:
            pylab.clf()

            plotCommand(self.emsa.getDataX(), self.emsa.getDataY())

            if self.duaneHuntLimit:
                pylab.axvline(x=self.duaneHuntLimit, linewidth=2, color='r')

            pylab.show()

def run():
    spectrum = Spectrum()

    projectPath = os.path.expanduser("~/works/prgrms/pythondev/SpectrumAnalyzer")

    filename = os.path.join(projectPath, "inputData/Spectrum 2.txt")

    spectrum.readFile(filename)

    spectrum.computeDuaneHuntLimit()

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=run)
