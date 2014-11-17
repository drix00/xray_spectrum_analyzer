#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import logging
import math
import os.path
import csv

# Third party modules.
import pylab
import numpy
from scipy.optimize import leastsq

# Local modules.
import pySpectrumFileFormat.emmff.emsaFormat as emsaFormat

import pyHendrixDemersTools.Colors as Colors

# Globals and constants variables.
def gaussianFitFunction(a, x):
    y = a[0]*numpy.exp(-numpy.log(2.0) * (numpy.power((x - a[1])/a[2], 2.0)))
    #y = a[0]*numpy.exp(-(numpy.power((x - a[1]), 2.0))/(2.0*numpy.power(a[2], 2.0)))

    return y

def linearBackground(a, x):
    y = a[0] + a[1]*x

    return y

class FitPeak(object):
    def __init__(self):
        self._height = 2.17E3
        self._position_keV = 15.7
        self._sigma_keV = 0.2

        self._b1 = 350.0
        self._b2 = 0.01

    def getPosition_keV(self):
        return self._position_keV

    def getIntensity(self):
        a = self.getGaussianParameters()

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))

        if intensity <= 0.0:
            logging.error("Intensity less than 0: %f", intensity)

            return None

        #intensity2 = sum(self.getPeakIntensities())
        #logging.debug("Intensity: %i", intensity)
        #logging.debug("Intensity: %i", intensity2)

        return intensity

    def setHeight(self, height):
        self._height = height

    def setPosition_keV(self, position_keV):
        self._position_keV = position_keV

    def setSigma_keV(self, sigma_keV):
        self._sigma_keV = sigma_keV

    def setGaussianParameters(self, a):
        self.setHeight(a[0])
        self.setPosition_keV(a[1])
        self.setSigma_keV(a[2])

    def getGaussianParameters(self):
        return self._height, self._position_keV, self._sigma_keV

    def setLinearBackgroundParameters(self, b):
        self.setLinearBackground(b[0], b[1])

    def setLinearBackground(self, a, m):
        self._b1 = a
        self._b2 = m

    def getLinearBackgroundParameters(self):
        return self._b1, self._b2

    def setEnergies(self, x):
        self._x = x

    def setIntensities(self, y):
        self._y = y

    def getEnergies(self):
        return self._x

    def getIntensities(self):
        return self._y

    def getFitIntensities(self):
        a = self.getGaussianParameters()
        b = self.getLinearBackgroundParameters()

        y = []

        for x in self._x:
            value = gaussianFitFunction(a, x)
            value += linearBackground(b, x)

            y.append(value)

        return y

    def getPeakIntensities(self):
        a = self.getGaussianParameters()

        y = []

        for x in self._x:
            value = gaussianFitFunction(a, x)

            y.append(value)

        return y

    def getBackground(self):
        a = self.getLinearBackgroundParameters()

        y = []

        for x in self._x:
            value = linearBackground(a, x)

            y.append(value)

        return y

    def _errorFunction(self, a, x, y):
        return (gaussianFitFunction(a[:3], x) + linearBackground(a[3:], x) - y)

    def _initFit(self):
        a = []

        a.extend(self.getGaussianParameters())

        a.extend(self.getLinearBackgroundParameters())

        return a, self._x, self._y

    def fit(self):
        ## Initial paramenter value
        a0, x, y = self._initFit()

        ## Fitting
        a, success = leastsq(self._errorFunction, a0, args=(x,y), maxfev=10000)

        if success == 1:
            logging.debug("Fit success: True")
        else:
            logging.debug("Fit success: False")

        logging.debug("Fit parameters: %s", str(a))

        self.setGaussianParameters(a[:3])

        self.setLinearBackgroundParameters(a[3:])

class ComputePeaksIntensities(object):
    def __init__(self, spectrumFilepath):
        self._initVariables()

        self._sprectrumFilepath = spectrumFilepath

        self._readSpectrumData(self._sprectrumFilepath)

    def _initVariables(self):
        self._spectrumFigureID = None

        self._peaksFigureID = {}

        self._peaks = {}

    def _readSpectrumData(self, spectrumFilepath):
        emsa = emsaFormat.EmsaFormat(spectrumFilepath)

        self._energies = emsa.getDataX()
        self._intensities = emsa.getDataY()

        logging.debug("Number energy: %i", len(self._energies))
        logging.debug("Number intensities: %i", len(self._intensities))

        assert len(self._energies) == len(self._intensities)

    def addPeak(self, label):
        self._peaks[label] = FitPeak()

        self._peaksFigureID.setdefault(label, None)

    def setPeakRange(self, label, energyMinimum_keV, energyMaximum_keV):
        x = []
        y = []

        for energy_keV, intensity in zip(self._energies, self._intensities):
            if energyMinimum_keV <= energy_keV <= energyMaximum_keV:
                x.append(energy_keV)
                y.append(intensity)

        x = numpy.array(x)
        y = numpy.array(y)

        self._peaks[label].setEnergies(x)
        self._peaks[label].setIntensities(y)

    def setPosition_keV(self, label, position_keV):
        self._peaks[label].setPosition_keV(position_keV)

    def fitPeak(self, label):
        self._peaks[label].fit()

    def fitAllPeaks(self):
        for label in self._peaks:
            self._peaks[label].fit()

    def displayAllPeaks(self):
        for label in self._peaks:
            self.displayPeak(label)

    def displayPeak(self, label):
        if self._peaksFigureID[label] == None:
            spectrumFigure = pylab.figure()
            self._peaksFigureID[label] = spectrumFigure.number

            logging.debug("Peak %s figure ID: %i", label, self._peaksFigureID[label])

        pylab.figure(num=self._peaksFigureID[label])

        pylab.clf()

        colors = Colors.GrayColors(4)

        x = self._peaks[label].getEnergies()
        y = self._peaks[label].getIntensities()

        yB = self._peaks[label].getBackground()

        yF = self._peaks[label].getFitIntensities()

        yP = self._peaks[label].getPeakIntensities()

        pylab.plot(x, y, '-', color=colors.next(), label='Experimental')
        pylab.plot(x, yF, '-', color=colors.next(), label='Fitted')
        pylab.plot(x, yP, '-', color=colors.next(), label='Peak')
        pylab.plot(x, yB, '-', color=colors.next(), label='Background')

        pylab.title(label)

        pylab.xlabel("X-ray energy (eV)")

        pylab.ylabel("Intensities")

        pylab.legend(loc='best')

    def displaySpectrum(self):
        if self._spectrumFigureID == None:
            spectrumFigure = pylab.figure()
            self._spectrumFigureID = spectrumFigure.number

            logging.debug("Spectrum figure ID: %i", self._spectrumFigureID)

        pylab.figure(num=self._spectrumFigureID)

        colors = Colors.GrayColors(1)

        pylab.plot(self._energies, self._intensities
                             , '-', color=colors.next())

        pylab.title(self._sprectrumFilepath)

        pylab.xlabel("X-ray energy (eV)")

        pylab.ylabel("Intensities")

        #pylab.legend(loc='best')

    def printRestults(self):

        # Header
        args = ("#Energy", "Line", "Intensity")
        print "%s\t%s\t%s" % args

        for label in self._peaks:
            energy_keV = self._peaks[label].getPosition_keV()

            intensity = self._peaks[label].getIntensity()

            args = (energy_keV, label, intensity)
            print "%0.3f\t%6s\t%i" % args

    def saveRestults(self):
        filepath, dummy_extention = os.path.splitext(self._sprectrumFilepath)

        filepath += ".csv"

        logging.debug("Results filepath: %s", filepath)

        writer = csv.writer(open(filepath, 'wb'))

        # Header
        row = ["#Energy", "Line", "Intensity"]
        writer.writerow(row)

        for label in self._peaks:
            energy_keV = self._peaks[label].getPosition_keV()

            intensity = self._peaks[label].getIntensity()

            row = [energy_keV, label, intensity]
            writer.writerow(row)

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
