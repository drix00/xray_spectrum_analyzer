#!/usr/bin/env python
"""
.. py:currentmodule:: console.FitLine
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Fit function for the x-ray lines.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyFitTools.fit.fitTools import _FitObject

# Project modules

# Globals and constants variables.

class FitLineKa1Ka2(_FitObject):
    def __init__(self, areaKa1=None, fractionKa2=None, muKa1=None, differenceKa2=None, sigmaKa=None):
        if areaKa1 is None:
            self._areaKa1Fixed = False
        else:
            self._areaKa1Fixed = True
        self._areaKa1 = areaKa1

        if fractionKa2 is None:
            self._fractionKa2Fixed = False
        else:
            self._fractionKa2Fixed = True
        self._fractionKa2 = fractionKa2

        if muKa1 is None:
            self._muKa1Fixed = False
        else:
            self._muKa1Fixed = True
        self._muKa1 = muKa1

        if differenceKa2 is None:
            self._differenceKa2Fixed = False
        else:
            self._differenceKa2Fixed = True
        self._differenceKa2 = differenceKa2

        if sigmaKa is None:
            self._sigmaKaFixed = False
        else:
            self._sigmaKaFixed = True
        self._sigmaKa = sigmaKa

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._areaKa1Fixed:
            self._areaKa1 = parameters[indexParameters]
            indexParameters +=1

        if not self._fractionKa2Fixed:
            self._fractionKa2 = parameters[indexParameters]
            indexParameters +=1

        if not self._muKa1Fixed:
            self._muKa1 = parameters[indexParameters]
            indexParameters +=1

        if not self._differenceKa2Fixed:
            self._differenceKa2 = parameters[indexParameters]
            indexParameters +=1

        if not self._sigmaKaFixed:
            self._sigmaKa = parameters[indexParameters]
            indexParameters +=1

        yFit = self.function(x)
        return yFit

    def function(self, x):
        gaussianKa1 = self._areaKa1*1.0/(self._sigmaKa*np.sqrt(2.0*np.pi)) * np.exp((-(x - self._muKa1)**2)/(2.0*self._sigmaKa**2))
        areaKa2 = self._areaKa1*self._fractionKa2
        muKa2 = self._muKa1 + self._differenceKa2
        sigmaKa2 = self._sigmaKa
        gaussianKa2 = areaKa2*1.0/(sigmaKa2*np.sqrt(2.0*np.pi)) * np.exp((-(x - muKa2)**2)/(2.0*sigmaKa2**2))
        return gaussianKa1 + gaussianKa2

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._areaKa1Fixed:
            numberParameters +=1
        if not self._fractionKa2Fixed:
            numberParameters +=1
        if not  self._muKa1Fixed:
            numberParameters +=1
        if not  self._differenceKa2Fixed:
            numberParameters +=1
        if not  self._sigmaKaFixed:
            numberParameters +=1

        return numberParameters


if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
