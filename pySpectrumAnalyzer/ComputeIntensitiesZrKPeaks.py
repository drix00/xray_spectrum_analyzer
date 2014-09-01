#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2292 $"
__svnDate__ = "$Date: 2011-03-21 11:29:50 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: ComputeIntensitiesZrKPeaks.py 2292 2011-03-21 15:29:50Z hdemers $"

# Standard library modules.
import os.path
import math
import logging

# Third party modules.
import pylab
from scipy.optimize import leastsq
import numpy

# Local modules.
import SpectrumFileFormatTools.emmff.emsaFormat as emsaFormat

# Globals and constants variables.
def gaussianFitFunction(a, x):
    y = a[0]*numpy.exp(-numpy.log(2.0) * (numpy.power((x - a[1])/a[2], 2.0)))
    #y = a[0]*numpy.exp(-(numpy.power((x - a[1]), 2.0))/(2.0*numpy.power(a[2], 2.0)))

    return y

def linearBackground(a, x):
    y = a[0] + a[1]*x

    return y

class ComputeIntensitiesZrKPeaks(object):
    def __init__(self, spectrumFilepath):
        self._display = False

        #print spectrumFilepath

        emsa = emsaFormat.EmsaFormat(spectrumFilepath)

        self.energies = emsa.getDataX()
        self.intensities = emsa.getDataY()

        logging.debug("Number energy: %i", len(self.energies))
        logging.debug("Number intensities: %i", len(self.intensities))

        assert len(self.energies) == len(self.intensities)

    def displaySpectum(self):
        pylab.figure()

        pylab.plot(self.energies, self.intensities)
        #pylab.semilogy(self.energies, self.intensities)

        pylab.xlabel("X-ray energy (keV)")

        pylab.ylabel("Intensity")

        #pylab.xlim((14.0, 19.0))
        #pylab.ylim(ymax=3000.0)

        self._display = True

    def displaySomething(self):
        if self._display:
            pylab.show()

    def errorFunction(self, a, x, y):
        return (gaussianFitFunction(a[:3],x) + linearBackground(a[3:], x) - y)

    def initFit(self, element, peak="Ka"):
        a = []

        if element == "C":
            if peak == "Ka":
                a.append(2.17E3)
                a.append(15.7)
                a.append(0.2)

                a.append(350.0)
                a.append(0.01)

                energyMinimum_keV = 0.18
                energyMaximum_keV = 0.35

        if element == "Zr":
            if peak == "Ka":
                a.append(2.17E3)
                a.append(15.7)
                a.append(0.2)

                a.append(350.0)
                a.append(0.01)

                energyMinimum_keV = 15.0
                energyMaximum_keV = 16.5

            if peak == "Kb":
                a.append(550.0)
                a.append(17.6)
                a.append(0.2)

                a.append(350.0)
                a.append(0.01)

                energyMinimum_keV = 16.5
                energyMaximum_keV = 19.0

            if peak == "L":
                a.append(550.0)
                a.append(2.1)
                a.append(0.2)

                a.append(350.0)
                a.append(0.01)

                energyMinimum_keV = 1.8
                energyMaximum_keV = 2.5

        if element == "Cu":
            if peak == "Ka":
                a.append(6.89E3)
                a.append(8.04)
                a.append(0.2)

                a.append(433.0)
                a.append(0.01)

                energyMinimum_keV = 7.5
                energyMaximum_keV = 8.5

            if peak == "Kb":
                a.append(1.2E3)
                a.append(8.89)
                a.append(0.2)

                a.append(356.0)
                a.append(0.01)

                energyMinimum_keV = 8.5
                energyMaximum_keV = 9.5

            if peak == "L":
                a.append(1.2E3)
                a.append(0.92)
                a.append(0.2)

                a.append(356.0)
                a.append(0.01)

                energyMinimum_keV = 0.8
                energyMaximum_keV = 1.15

        if element == "Mn":
            if peak == "Ka":
                a.append(4.36E4)
                a.append(5.89)
                a.append(0.2)

                a.append(500.0)
                a.append(0.01)

                energyMinimum_keV = 5.6
                energyMaximum_keV = 6.2

            if peak == "Kb":
                a.append(6.3E3)
                a.append(6.48)
                a.append(0.2)

                a.append(733.0)
                a.append(0.01)

                energyMinimum_keV = 6.2
                energyMaximum_keV = 6.9

            if peak == "L":
                a.append(1.2E3)
                a.append(0.64)
                a.append(0.2)

                a.append(356.0)
                a.append(0.01)

                energyMinimum_keV = 0.57
                energyMaximum_keV = 0.74

        if element == "Al":
            if peak == "Ka":
                a.append(4.36E4)
                a.append(1.47)
                a.append(0.2)

                a.append(800.0)
                a.append(0.01)

                energyMinimum_keV = 1.1
                energyMaximum_keV = 1.65

        x = []
        y = []

        for energy_keV, intensity in zip(self.energies, self.intensities):
            if energyMinimum_keV <= energy_keV <= energyMaximum_keV:
                x.append(energy_keV)
                y.append(intensity)

        x = numpy.array(x)
        y = numpy.array(y)

        return a, x, y

    def fit(self, element, peak):
        ## Initial paramenter value
        a0, x, y = self.initFit(element, peak)

        ## Fitting
        a, dummy_success = leastsq(self.errorFunction, a0, args=(x,y), maxfev=10000)

        #print a, success

        return a, x, y

    def getCKaIntensity(self):
        a, dummy_x, dummy_y = self.fit("C", "Ka")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getZrLIntensity(self):
        a, dummy_x, dummy_y = self.fit("Zr", "L")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getZrKaIntensity(self):
        a, dummy_x, dummy_y = self.fit("Zr", "Ka")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getZrKbIntensity(self):
        a, dummy_x, dummy_y = self.fit("Zr", "Kb")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        logging.debug("Zr Kb intensity: %f", intensity)

        return intensity, error

    def getCuLIntensity(self):
        a, dummy_x, dummy_y = self.fit("Cu", "L")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getCuKaIntensity(self):
        a, dummy_x, dummy_y = self.fit("Cu", "Ka")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getCuKbIntensity(self):
        a, dummy_x, dummy_y = self.fit("Cu", "Kb")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getMnKIntensity(self):

        intensity, error = self.getMnKaIntensity()

        intensityKb, errorKb = self.getMnKbIntensity()

        if intensityKb is not None:
            intensity += intensityKb

            error += errorKb

        return intensity, error

    def getAlKaIntensity(self):
        a, dummy_x, dummy_y = self.fit("Al", "Ka")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        logging.debug("Mn Ka intensity: %f", intensity)

        return intensity, error

    def getMnLIntensity(self):
        a, dummy_x, dummy_y = self.fit("Mn", "L")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def getMnKaIntensity(self):
        a, dummy_x, dummy_y = self.fit("Mn", "Ka")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        logging.debug("Mn Ka intensity: %f", intensity)

        return intensity, error

    def getMnKbIntensity(self):
        a, dummy_x, dummy_y = self.fit("Mn", "Kb")

        intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(math.pi/math.log(2))
        #intensity = a[0] * abs(a[2]*1.0E2) * math.sqrt(2.0*math.pi)
        #intensity = a[0]

        if intensity <= 0.0:
            return None, None

        error = 3.0*math.sqrt(intensity)

        return intensity, error

    def displayZrKaFit(self):
        self.displayFit("Zr", "Ka")

    def displayZrKbFit(self):
        self.displayFit("Zr", "Kb")

    def displayFit(self, element, peak):
        a, x, y = self.fit(element, peak)

        func1 = gaussianFitFunction

        func2 = linearBackground

        a1 = a[:3]
        a2 = a[3:]

        yFit = [func1(a1, xx) + func2(a2, xx) for xx in x]

        #yFitG = [func1(a1, xx) for xx in x]

        yFitLB = [func2(a2, xx) for xx in x]

        pylab.figure()

        pylab.plot(x, y, label="Data")

        pylab.plot(x, yFit, label="Fit")

        pylab.plot(x, yFitLB, label="LB")

        pylab.xlabel("X-ray energy (keV)")

        pylab.ylabel("Intensity")

        pylab.legend(loc='best')

        self._display = True

def run():
    #baseFolderpath = os.path.expanduser("~/works/results/experiments/sem/VP-SEM/080125/30keV")

    #filenames = ["Spectrum 3.txt", "Spectrum 8.txt"]
    #filenames = ["Spectrum 3.txt"]
    #filenames = ["Spectrum 8.txt"]

    baseFolderpath = os.path.expanduser("~/works/results/experiments/sem/VP-SEM/080127/30keV")
    #filenames = ["Spectrum 17.txt"]
    filenames = ["Spectrum 22.txt"]

    for filename in filenames:
        filepath = os.path.join(baseFolderpath, filename)

        computeIntensitiesZrKPeaks = ComputeIntensitiesZrKPeaks(filepath)

        #computeIntensitiesZrKPeaks.displayZrKaFit()

        #computeIntensitiesZrKPeaks.displayZrKbFit()

        intZrKa = computeIntensitiesZrKPeaks.getZrKaIntensity()[0]

        intZrKb = computeIntensitiesZrKPeaks.getZrKbIntensity()[0]

        print "Ka: ", intZrKa

        print "Kb: ", intZrKb

        #intensity = float(computeIntensitiesZrKPeaks.getCuKaIntensity()[0])
        #intensity += float(computeIntensitiesZrKPeaks.getCuKbIntensity()[0])

        #print "Cu K: %0.1f" % (intensity)

        #computeIntensitiesZrKPeaks.displayFit("Cu", "Ka")

        #computeIntensitiesZrKPeaks.displayFit("Cu", "Kb")

        intMnK = float(computeIntensitiesZrKPeaks.getMnKaIntensity()[0])
        intMnK += float(computeIntensitiesZrKPeaks.getMnKbIntensity()[0])

        print "Mn K: %0.1f" % (intMnK)

        ratioZrKa = 0.80*(intZrKa/intMnK)*28.294

        ratioZrKb = 0.80*(intZrKb/intMnK)*147.199

        print "%0.3f %0.3f" % (ratioZrKa, ratioZrKb)

        intMnK = 721911.8

        ratioZrKa = 0.80*(intZrKa/intMnK)*28.294

        ratioZrKb = 0.80*(intZrKb/intMnK)*147.199

        print "%0.3f %0.3f" % (ratioZrKa, ratioZrKb)
        #computeIntensitiesZrKPeaks.displaySpectum()

        computeIntensitiesZrKPeaks.displaySomething()

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=run)
