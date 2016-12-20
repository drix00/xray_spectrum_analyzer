#!/usr/bin/env python
"""
.. py:currentmodule:: SpectrumAnalyzer
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Console version of spectrum analyzer.
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
import logging
import os.path
import math
import csv

# Third party modules.
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import OffsetFrom
import numpy as np
from scipy.interpolate import interp1d

from lmfit import minimize, Parameters

# Local modules.
import pySpectrumFileFormat.emmff.emsa as emsa
import pySpectrumFileFormat.emmff.emsaFormat as emsaFormat
import pySpectrumFileFormat.Bruker.ExportedCsvFile as ExportedCsvFile

from pySpectrumAnalyzer import get_current_module_path, createPath
from pySpectrumAnalyzer import saveFigureData

from pySpectrumAnalyzer.tools.FitPolynomialFunction import PolynomialFirstDegreeFunction
from pySpectrumAnalyzer.tools.FitGaussianFunction import GaussianFunction

# Project modules
import pySpectrumAnalyzer.ui.console.XrayLineReferenceManager as XrayLineReferenceManager

# Globals and constants variables.
DEBUG = False

FIT_METHOD_PEAK = "fitMethodPeak"
FIT_METHOD_PEAK_FAMILY = "fitMethodPeakFamily"
FIT_METHOD_ROI = "fitMethodRoi"
FIT_METHOD_SPECTRUM = "fitMethodSpectrum"

ROI_CARBON_DOUBLE_PEAKS = "Roi DC K"

class PeakIntensity(object):
    _numericFactor = 2.0 * math.sqrt(2.0 * math.log(2.0))

    def __init__(self, xData, yData, yBackground, position_keV, sigma_keV, label):
        self.xData = xData
        self.yData = yData
        self.yBackground = yBackground
        self.position_keV = position_keV
        self.sigma_keV = sigma_keV
        self.label = label

    def countsFromFixedWidth(self, width_keV):
        v1 = self.position_keV - width_keV/2.0
        v2 = self.position_keV + width_keV/2.0
        maskArray = np.ma.masked_outside(self.xData, v1, v2)

        counts = np.sum(self.yData[~maskArray.mask])
        return counts

    def countsBackgroundFromFixedWidth(self, width_keV):
        v1 = self.position_keV - width_keV/2.0
        v2 = self.position_keV + width_keV/2.0
        maskArray = np.ma.masked_outside(self.xData, v1, v2)

        counts = np.sum(self.yBackground[~maskArray.mask])
        return counts

    @property
    def xData(self):
        return self._xData
    @xData.setter
    def xData(self, xData):
        self._xData = np.array(xData)

    @property
    def yData(self):
        return self._yData
    @yData.setter
    def yData(self, yData):
        self._yData = np.array(yData)

    @property
    def yBackground(self):
        return self._yBackground
    @yBackground.setter
    def yBackground(self, yBackground):
        self._yBackground = np.array(yBackground)

    @property
    def counts(self):
        return np.sum(self.yData)

    @property
    def countsBackground(self):
        return np.sum(self.yBackground)

    @property
    def sigma_keV(self):
        return self._sigma_keV
    @sigma_keV.setter
    def sigma_keV(self, sigma_keV):
        self._sigma_keV = sigma_keV

    @property
    def position_keV(self):
        return self._position_keV
    @position_keV.setter
    def position_keV(self, position_keV):
        self._position_keV = position_keV

    @property
    def fwhm_keV(self):
        return self.sigma_keV * self._numericFactor

    @property
    def fwhm_eV(self):
        return self.fwhm_keV * 1.0e3

    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, label):
        self._label = label


class DetectorFunction(object):
    def __init__(self, electronicNoise_eV, FanoFactor):
        self._electronicNoise_eV = electronicNoise_eV
        self._FanoFactor = FanoFactor
        self._electronHolePair_eV = 3.8
        self._numericFactor = 2.0 * math.sqrt(2.0 * math.log(2.0))

    def getFwhm_eV(self, xrayEnergy_eV):
        term1 = self._electronicNoise_eV**2
        term2 = self._numericFactor*self._numericFactor*self._electronHolePair_eV*self._FanoFactor*xrayEnergy_eV
        fwhm_eV = math.sqrt(term1 + term2)

        return fwhm_eV

    def getSigma_keV(self, xrayEnergy_keV):
        xrayEnergy_eV = xrayEnergy_keV*1.0e3
        fwhm_eV = self.getFwhm_eV(xrayEnergy_eV)
        fwhm_keV = fwhm_eV/1.0e3

        sigma_keV = fwhm_keV/self._numericFactor

        return sigma_keV

    def getElectronicNoise_eV(self):
        return self._electronicNoise_eV

class Roi(object):
    def __init__(self, label, energyRange_keV, no_background=False):
        self.label = label
        self.energyRange_keV = energyRange_keV
        self.no_background = no_background

    def displayRoi(self, xData, yData):
        xData = np.array(xData)
        yData = np.array(yData)

        eMin_keV, eMax_keV = self.energyRange_keV

        color = 'g'
        yMin = 0.0

        plt.axvspan(eMin_keV, eMax_keV, ymin=yMin, ymax=1.0, transform=plt.gca().transData,
                    color=color, linewidth=2, zorder=-20, alpha=0.2)

    def getRoiData(self, xData, yData):
        eMin_keV, eMax_keV = self.energyRange_keV
        maskArray = np.ma.masked_outside(xData, eMin_keV, eMax_keV)
        xRoi = xData[~maskArray.mask].copy()
        yRoi = yData[~maskArray.mask].copy()

        return xRoi, yRoi

    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, label):
        self._label = label

    @property
    def energyRange_keV(self):
        return self._energyRange_keV
    @energyRange_keV.setter
    def energyRange_keV(self, energyRange_keV):
        self._energyRange_keV = energyRange_keV

class SpectrumAnalyzer(object):
    def __init__(self, outputPath=None, configurationFilepath=None, keepGraphic=True):
        if outputPath is not None:
            self._outputPath = createPath(outputPath)

        self._configurationFilepath = configurationFilepath
        self._keepGraphic = keepGraphic

        self._lineRefManager = XrayLineReferenceManager.XrayLineReferenceManager()

        self.showEdgeMarkers = False
        self.showMajorLineMarkers = True
        self.showMinorLineMarkers = False
        self.showSatelliteLineMarkers = False
        self.showSiEscapeMarkers = False
        self.showRois = True
        self.showFittedPeaks = True
        self.exportRois = False
        self.hasDoubleCarbonPeak = False
        self.maximumEnergy_keV = None

        self.fitMethod = FIT_METHOD_PEAK

        self._rois = {}

        self._requiredPeaks = []
        self._omittedPeaks = []

        self._spectrumFilepath = None
        self._spectrum = None

        self._maximumPositionError_keV = 0.010

    def addElement(self, symbol):
        self._lineRefManager.addElement(symbol)

    def addRequiredPeak(self, symbol, peakLabel):
        self._requiredPeaks.append((symbol, peakLabel))

    def addOmittedPeak(self, symbol, peakLabel):
        self._omittedPeaks.append((symbol, peakLabel))

    def addRoi(self, label, energyRange_keV, no_background=False):
        if self.maximumEnergy_keV is not None and energyRange_keV[0] > self.maximumEnergy_keV:
            logging.info("Roi not added, energy range greater than the primary energy")
        else:
            roi = Roi(label, energyRange_keV, no_background)
            self._rois[label] = roi

    def readSpectrum(self, spectrumFilepath):
        logging.info("Read spectrum file: %s", spectrumFilepath)

        self._spectrumFilepath = spectrumFilepath
        self._spectrum = emsaFormat.EmsaFormat(spectrumFilepath)

    def readExportedMcXraySpectrum(self, spectrumFilepath):
        self._spectrumFilepath = spectrumFilepath
        lines = open(spectrumFilepath, 'rb').readlines()

        xdata = []
        ydata = []
        for line in lines[2:-1]:
            items = line.split()
            assert len(items) == 2

            xdata.append(float(items[0]))
            ydata.append(float(items[1]))

        self._spectrum = emsa.EmsaReader()
        self._spectrum.xdata = xdata
        self._spectrum.ydata = ydata

    def readExportedBrukerSpectrum(self, spectrumFilepath):
        logging.info("Reading spectrum: %s", spectrumFilepath)

        self._spectrumFilepath = spectrumFilepath

        spectrum = ExportedCsvFile.readSpectrum(spectrumFilepath)

        self._spectrum = emsa.EmsaReader()
        self._spectrum.xdata = spectrum.energies_keV
        self._spectrum.ydata = spectrum.countsList

        self.maximumEnergy_keV = spectrum.primaryEnergy_keV

    def plotSpectrum(self, figure=None, yLog=False):
        xData = np.array(self._spectrum.getDataX())
        if self._spectrum.getXUnits() == 'eV':
            xData *= 1.0e-3

        yData = np.array(self._spectrum.getDataY())

        if figure is None:
            figure = plt.figure()
        else:
            figure.clear()

        axes = figure.add_subplot(111)

        if yLog:
            axes.semilogy(xData, yData)
        else:
            axes.plot(xData, yData)

        if self.showEdgeMarkers:
            self._addEdgeMarkers()

        if self.showMajorLineMarkers:
            self._addMajorLineMarkers()

        if self.showMinorLineMarkers:
            self._addMinorLineMarkers()

        if self.showSatelliteLineMarkers:
            self._addSatelliteLineMarkers()

        if self.showSiEscapeMarkers:
            self._addSiEscapeMarkers()

        if self.showRois:
            self._addRois(xData, yData)

        self._addRequiredLines()

        axes.set_xlabel("Energy (keV)")
        axes.set_ylabel("Counts")

        if self.maximumEnergy_keV is not None:
            xMin = np.min(xData)
            axes.set_xlim((xMin, self.maximumEnergy_keV))

    def fitRoi(self, roiName):
        xData = np.array(self._spectrum.xdata)
        yData = np.array(self._spectrum.ydata)
        roi = self._rois[roiName]
        self._fitRoi(roi, xData, yData)

    def analyze(self, spectrumFilepath):
        logging.info("Analyze spectrum: %s", spectrumFilepath)

        if self._spectrumFilepath is None:
            self.readSpectrum(spectrumFilepath)

        #self.plotSpectrum()

        xData = np.array(self._spectrum.getDataX())
        if self._spectrum.getXUnits() == 'eV':
            xData *= 1.0e-3
        yData = np.array(self._spectrum.getDataY())
        peakIntensities = []
        for roiName in self._rois:
            roi = self._rois[roiName]
            peakIntensitiesRoi = self._fitRoi(roi, xData, yData)
            peakIntensities.extend(peakIntensitiesRoi)

        self.savePeakIntensities(peakIntensities)

        del peakIntensitiesRoi
        del self._spectrum
        del xData
        del yData

    def saveSpectrum(self, isLogScale=False):
        logging.info("Save spectrum")

        xData = np.array(self._spectrum.getDataX())
        if self._spectrum.getXUnits() == 'eV':
            xData *= 1.0e-3
        yData = np.array(self._spectrum.getDataY())

        figure = plt.figure()

        if isLogScale:
            plt.semilogy(xData, yData)
        else:
            plt.plot(xData, yData)

        if self.showEdgeMarkers:
            self._addEdgeMarkers()

        if self.showMajorLineMarkers:
            self._addMajorLineMarkers()

        if self.showMinorLineMarkers:
            self._addMinorLineMarkers()

        if self.showSatelliteLineMarkers:
            self._addSatelliteLineMarkers()

        if self.showSiEscapeMarkers:
            self._addSiEscapeMarkers()

        if self.showRois:
            self._addRois(xData, yData)

        self._addRequiredLines()

        plt.xlabel("Energy (keV)")
        plt.ylabel("Counts")

        if self.maximumEnergy_keV is not None and len(xData) > 0:
            xMin = np.min(xData)
            plt.xlim((xMin, self.maximumEnergy_keV))

        spectrumFilename = os.path.basename(self._spectrumFilepath)
        graphicFilename, _extension = os.path.splitext(spectrumFilename)

        if isLogScale:
            graphicFilename += '_Log'

        for extension in ['.png']:
            graphicFilepath = os.path.join(self._outputPath, graphicFilename+extension)
            plt.savefig(graphicFilepath)

        del xData
        del yData

        plt.clf()
        plt.close()
        del figure

    def saveRois(self):
        xData = np.array(self._spectrum.xdata)
        yData = np.array(self._spectrum.ydata)

        for roiName in self._rois:
            roi = self._rois[roiName]
            xRoi, yRoi = roi.getRoiData(xData, yData)
            self._saveRoi(roi, xRoi, yRoi, roiName)

    def _saveRoi(self, roi, xData, yData, roiName, isLogScale=False):
        figure = plt.figure()

        if isLogScale:
            plt.semilogy(xData, yData)
        else:
            plt.plot(xData, yData)

        if self.showEdgeMarkers:
            self._addEdgeMarkers()

        if self.showMajorLineMarkers:
            self._addMajorLineMarkers()

        if self.showMinorLineMarkers:
            self._addMinorLineMarkers()

        if self.showSatelliteLineMarkers:
            self._addSatelliteLineMarkers()

        if self.showSiEscapeMarkers:
            self._addSiEscapeMarkers()

        if self.showRois:
            self._addRois(xData, yData)

        plt.xlabel("Energy (keV)")
        plt.ylabel("Counts")

        plt.ylim(ymin=0.0)

        spectrumFilename = os.path.basename(self._spectrumFilepath)
        graphicFilename, _extension = os.path.splitext(spectrumFilename)
        graphicFilename += "_%s" % (roiName)

        if isLogScale:
            graphicFilename += '_Log'

        for extension in ['.png']:
            graphicFilepath = os.path.join(self._outputPath, graphicFilename+extension)
            plt.savefig(graphicFilepath)

        plt.clf()
        plt.close()
        del figure

    def _addEdgeMarkers(self):
        color = 'r'
        yFraction = 0.2

        for position_keV, label in self._lineRefManager.getAbsorptionEdges():
            xMin, xMax = plt.xlim()
            if xMin <= position_keV and position_keV <= xMax:
                t = plt.axvline(x=position_keV, ymin=0, ymax=yFraction, color=color, label=label, linewidth=4)
                plt.annotate(label, (0.2, 0.2), xycoords=OffsetFrom(t, (0.0, 1.1), unit="points"), color=color,
                             horizontalalignment='center', rotation='horizontal', backgroundcolor='w')

    def _addMajorLineMarkers(self):
        color = 'k'
        lines = self._lineRefManager.getMajorLines()

        self._addLineMarkers(color, lines)

    def _addRequiredLines(self):
        color = 'k'
        lines = self._lineRefManager.getLines(self._requiredPeaks)

        self._addLineMarkers(color, lines)

    def _addMinorLineMarkers(self):
        color = 'k'
        lines = self._lineRefManager.getMinorLines()
        self._addLineMarkers(color, lines)

    def _addSatelliteLineMarkers(self):
        color = 'k'
        lines = self._lineRefManager.getSatelliteLines()
        self._addLineMarkers(color, lines)

    def _addSiEscapeMarkers(self):
        color = 'g'
        yFraction = 0.2

        peaks = self._lineRefManager.getSiEscapePeaks()
        for position_keV, label in peaks:
            xMin, xMax = plt.xlim()
            if xMin <= position_keV and position_keV <= xMax:
                t = plt.axvline(x=position_keV, ymin=0, ymax=yFraction, color=color, label=label, linewidth=4)
                plt.annotate(label, (0.2, 0.2), xycoords=OffsetFrom(t, (0.0, 1.1), unit="points"), color=color,
                             horizontalalignment='center', rotation='horizontal', backgroundcolor='w')

    def _addLineMarkers(self, color, lines):
        for position_keV, fraction, label in lines:
            self._plotFixScale(position_keV, fraction, label, color)

    def _plotFixScale(self, position_keV, fraction, label, color):
            #yMin, yMax = plt.ylim()
            #yFraction = yMax*fraction
            xMin, xMax = plt.xlim()
            if xMin <= position_keV and position_keV <= xMax:
#                t = plt.axvspan(xmin=position_keV, xmax=position_keV, ymin=0, ymax=yFraction, color=color,
#                                label=label, linewidth=1, transform=plt.gca().transData)
                t = plt.axvline(x=position_keV, ymin=0, ymax=fraction, color=color, label=label, linewidth=1)
                plt.annotate(label, (0.2, 0.2), xycoords=OffsetFrom(t, (0.0, 1.0), unit="points"), color=color,
                             horizontalalignment='center', rotation='horizontal', verticalalignment='top',
                             backgroundcolor='w')

    def _addRois(self, xData, yData):
        logging.info("_addRois")

        for roiName in self._rois:
            roi = self._rois[roiName]
            roi.displayRoi(xData, yData)

    def _fitRoi(self, roi, xData, yData):
        xRoi, yRoi = roi.getRoiData(xData, yData)
        if len(xRoi) <= 0:
            logging.warning("No experimental data for roi: %s", roi.label)
            return []

        roiPeaks = self.getRoiPeaks(roi)

        if self.fitMethod == FIT_METHOD_PEAK:
            peakIntensities = self._fitPeaks(xRoi, yRoi, roiPeaks, roi.label, no_background=roi.no_background)
        elif self.fitMethod == FIT_METHOD_PEAK_FAMILY:
            peakIntensities = self._fitPeaksFamily(xRoi, yRoi, roiPeaks, roi.label, no_background=roi.no_background)
        elif self.fitMethod == FIT_METHOD_ROI:
            peakIntensities = self._fitRoiPeaks(xRoi, yRoi, roiPeaks, roi.label)
        elif self.fitMethod == FIT_METHOD_SPECTRUM:
            peakIntensities = self._fitSpectrumPeaks(xRoi, yRoi, roiPeaks, roi.label)

        return peakIntensities

    def getRoiPeaks(self, roi):
        eMin_keV, eMax_keV = roi.energyRange_keV

        lines = self._lineRefManager.getMajorLines()
        lines.extend(self._lineRefManager.getLines(self._requiredPeaks))
        omittedLines = self._lineRefManager.getLines(self._omittedPeaks)

        for omittedLine in omittedLines:
            try:
                lines.remove(omittedLine)
            except ValueError as message:
                logging.info(omittedLine)
                logging.warning(message)

        fractionTotal = 0.0
        for position_keV, fraction, label in lines:
            if eMin_keV <= position_keV <= eMax_keV:
                fractionTotal += fraction

        roiPeaks = []
        for position_keV, fraction, label in lines:
            if eMin_keV <= position_keV <= eMax_keV:
                roiPeaks.append((position_keV, fraction/fractionTotal, label))

        # Add strobed noise peak
        if eMin_keV <= 0.0 <= eMax_keV:
            label = "n"
            roiPeaks.append((0.0, 1.0, label))

        # Add carbon double peak.
        if self.hasDoubleCarbonPeak and eMin_keV <= 0.15 <= eMax_keV:
            label = "CD"
            roiPeaks.append((0.15, 1.0, label))

        return roiPeaks

    def _fitPeaks(self, xRoi, yRoi, roiPeaks, roiLabel, no_background=False):
        parameters = Parameters()

        assert len(xRoi) > 0, roiLabel
        assert len(yRoi) > 0, roiLabel

        aGuess, bGuess = self._computeLinearBackgroundGuess(xRoi, yRoi)
        if self.hasDoubleCarbonPeak and roiLabel == ROI_CARBON_DOUBLE_PEAKS:
            parameters.add('lb_a', value=aGuess, vary=False)
            parameters.add('lb_b', value=bGuess, vary=False)
        else:
            parameters.add('lb_a', value=aGuess, vary=True)
            parameters.add('lb_b', value=bGuess, vary=True)
            
        roiMax = np.max(yRoi)

        for position_keV, fraction, label in roiPeaks:
            sigmaGuess = self._detector.getSigma_keV(position_keV)
            key = "%s_%s" % (label.replace(' ', '_'), "sigma")
            if label == 'n':
                parameters.add(key, value=sigmaGuess, min=0.0)
            elif self.hasDoubleCarbonPeak and (label.startswith("C K") or label == "CD"):
                parameters.add(key, value=sigmaGuess, min=sigmaGuess*0.9)
            else:
                parameters.add(key, value=sigmaGuess, min=sigmaGuess*0.8, max=sigmaGuess*1.2)

            areaGuess = roiMax*fraction*sigmaGuess*np.sqrt(2.0 * np.pi)
            key = "%s_%s" % (label.replace(' ', '_'), "area")
            parameters.add(key, value=areaGuess, min=0.0)

            key = "%s_%s" % (label.replace(' ', '_'), "position")
            if label == 'n':
                parameters.add(key, value=position_keV)
            else:
                positionMin_keV = position_keV - self._maximumPositionError_keV
                positionMax_keV = position_keV + self._maximumPositionError_keV
                parameters.add(key, value=position_keV, min=positionMin_keV, max=positionMax_keV)

        def functionBackground(parameters, x):
            a = parameters['lb_a'].value
            b = parameters['lb_b'].value
            linearBackground = PolynomialFirstDegreeFunction(a=a, b=b)

            return linearBackground(x)

        def peakFunction(parameters, x, baseKey):
            key = "%s_%s" % (baseKey, "area")
            area = parameters[key].value

            key = "%s_%s" % (baseKey, "position")
            mu = parameters[key].value

            key = "%s_%s" % (baseKey, "sigma")
            sigma = parameters[key].value

            peakFunction = GaussianFunction(area=area, mu=mu, sigma=sigma)

            return peakFunction(x)

        def functionModel(parameters, x):
            model = functionBackground(parameters, x)

            for position_keV, fraction, label in roiPeaks:
                baseKey = label.replace(' ', '_')
                model += peakFunction(parameters, x, baseKey)

            return model

        def residual(parameters, x, data):
            model = functionModel(parameters, x)
            return (data-model)

        result  = minimize(residual, parameters, args=(xRoi, yRoi))

        #result  = minimize(residual, parameters, args=(xRoi, yRoi))

        xFit = xRoi
        yFit = functionModel(result.params, xFit)

        #logging.info("Fit succes?: %s", result.success)
        #logging.info("Number evaluation: %i", result.nfev)
        #logging.info("Message: %s", result.message)
        #logging.info("Residual: %s", calculateR2(yRoi, yFit) )
        #logging.info("chi2: %s", result.chisqr)
        #logging.info("reduced chi2: %s", result.redchi)

        logging.info('Best-Fit Values:')
        for name, par in result.params.items():
            logging.info('  %s = %.4f +/- %.4f', name, par.value, par.stderr)

        left= 0.1
        width = 1.0 - 2.0 * left

        bottom_h = 0.1
        height_h = 0.1
        bottom = bottom_h + height_h + 0.02
        height = 1.0 - bottom - 0.1

        assert (left + width) <= 1.0
        assert (bottom + height) <= 1.0

        rectA_profile = [left, bottom, width, height]
        rectA_residual = [left, bottom_h, width, height_h]

        figure = plt.figure()
        #figure.clf()
        figure.suptitle(roiLabel, fontsize=16)
        axScatter = figure.add_axes(rectA_profile)

        axScatter.plot(xRoi, yRoi, '.', label='Data')
        axScatter.plot(xFit, yFit, label='Fit')

        yFitLB = functionBackground(result.params, xFit)
        axScatter.plot(xFit, yFitLB, label='Fit LB')

        for position_keV, fraction, label in roiPeaks:
            baseKey = label.replace(' ', '_')
            yFitP = peakFunction(result.params, xFit, baseKey)
            axScatter.plot(xFit, yFitP, label='Fit %s' % (label))

        axScatter.set_xlim(xRoi[0], xRoi[-1])
        axScatter.set_xticks([])

        axScatter.legend(loc='best')

        residual = yRoi - yFit
        axHistx = figure.add_axes(rectA_residual)
        axHistx.plot(xFit, residual, label='Residual')
        axHistx.set_xlim(xRoi[0], xRoi[-1])
        axHistx.locator_params(axis='y', tight=True, nbins=4)

        basefilepath, _extension = os.path.splitext(self._spectrumFilepath)
        _path, basename = os.path.split(basefilepath)
        basefilepath = os.path.join(self._outputPath, basename)
        roiFitFigureFilepath = basefilepath + '_' + roiLabel.replace(" ", '_')
        for extension in ['.png']:
            figure.savefig(roiFitFigureFilepath+extension)

        if self.exportRois:
            saveFigureData(roiFitFigureFilepath+".csv")

        plt.clf()
        plt.close()
        del figure

        peakIntensities = []

        for _position_keV, _fraction, label in roiPeaks:
            baseKey = label.replace(' ', '_')
            yFitP = peakFunction(result.params, xFit, baseKey)
            yBackground = functionBackground(result.params, xFit)

            key = "%s_%s" % (baseKey, "position")
            position_keV = result.params[key].value
            key = "%s_%s" % (baseKey, "sigma")
            sigma_keV = result.params[key].value

            peakIntensity = PeakIntensity(xFit, yFitP, yBackground, position_keV, sigma_keV, label)
            peakIntensities.append(peakIntensity)

        return peakIntensities

    def _fitPeaksFamily(self, xRoi, yRoi, roiPeaks, roiLabel, no_background=False):
        parameters = Parameters()

        assert len(xRoi) > 0, roiLabel
        assert len(yRoi) > 0, roiLabel

        if not no_background:
            aGuess, bGuess = self._computeLinearBackgroundGuess(xRoi, yRoi)
            parameters.add('lb_a', value=aGuess, vary=True)
            parameters.add('lb_b', value=bGuess, vary=True)

        roiMax = np.max(yRoi)

        peak_family_list = self._get_peak_family_list(roiPeaks)

        for peak_family_label in peak_family_list:
            print(peak_family_label)

            family_position_keV = None
            for position_keV, fraction, label in peak_family_list[peak_family_label]:
                if label.endswith('a1') or peak_family_label == 'n':
                    family_position_keV = position_keV
                    family_height = interp1d(xRoi, yRoi)(position_keV)

            parameters.add(peak_family_label+"_height", value=roiMax, min=0.0)

            if peak_family_label == 'n':
                parameters.add(peak_family_label+"_position", value=position_keV)
            else:
                positionMin_keV = family_position_keV - self._maximumPositionError_keV
                positionMax_keV = family_position_keV + self._maximumPositionError_keV
                parameters.add(peak_family_label+"_position", value=family_position_keV, min=positionMin_keV, max=positionMax_keV)

        def functionBackground(parameters, x):
            a = parameters['lb_a'].value
            b = parameters['lb_b'].value
            linearBackground = PolynomialFirstDegreeFunction(a=a, b=b)

            return linearBackground(x)

        def functionModel(parameters, x):
            if not no_background:
                model = functionBackground(parameters, x)
            else:
                model = None

            for peak_family_label in peak_family_list:
                family_height = parameters[peak_family_label+"_height"]
                family_position_keV = parameters[peak_family_label+"_position"]

                family_positionRef_keV = None
                for position_keV, fraction, label in peak_family_list[peak_family_label]:
                    if label.endswith('a1') or peak_family_label == 'n':
                        family_positionRef_keV = position_keV

                delta_position = family_positionRef_keV - family_position_keV
                for position_keV, fraction, label in peak_family_list[peak_family_label]:
                    mu = position_keV - delta_position
                    sigma = self._detector.getSigma_keV(position_keV)
                    area = family_height*fraction*sigma*np.sqrt(2.0 * np.pi)
                    peakFunction = GaussianFunction(area=area, mu=mu, sigma=sigma)
                    if model is not None:
                        model += peakFunction(x)
                    else:
                        model = peakFunction(x)

            return model

        def residual(parameters, x, data):
            model = functionModel(parameters, x)
            return (data-model)

        result  = minimize(residual, parameters, args=(xRoi, yRoi))

        xFit = xRoi
        yFit = functionModel(result.params, xFit)

        logging.info('Best-Fit Values:')
        for name, par in result.params.items():
            logging.info('  %s = %.4f +/- %.4f', name, par.value, par.stderr)

        left= 0.1
        width = 1.0 - 2.0 * left

        bottom_h = 0.1
        height_h = 0.1
        bottom = bottom_h + height_h + 0.02
        height = 1.0 - bottom - 0.1

        assert (left + width) <= 1.0
        assert (bottom + height) <= 1.0

        rectA_profile = [left, bottom, width, height]
        rectA_residual = [left, bottom_h, width, height_h]

        figure = plt.figure()
        #figure.clf()
        figure.suptitle(roiLabel, fontsize=16)
        axScatter = figure.add_axes(rectA_profile)

        axScatter.plot(xRoi, yRoi, '.', label='Data')
        axScatter.plot(xFit, yFit, label='Fit')

        if not no_background:
            yFitLB = functionBackground(result.params, xFit)
            axScatter.plot(xFit, yFitLB, label='Fit LB')

        for peak_family_label in peak_family_list:
            family_height = result.params[peak_family_label+"_height"]
            family_position_keV = result.params[peak_family_label+"_position"]

            yFitP = np.zeros_like(xFit)
            family_positionRef_keV = None
            for position_keV, fraction, label in peak_family_list[peak_family_label]:
                if label.endswith('a1') or peak_family_label == 'n':
                    family_positionRef_keV = position_keV

            delta_position = family_positionRef_keV - family_position_keV
            for position_keV, fraction, label in peak_family_list[peak_family_label]:
                mu = position_keV - delta_position
                sigma = self._detector.getSigma_keV(position_keV)
                area = family_height*fraction*sigma*np.sqrt(2.0 * np.pi)
                peakFunction = GaussianFunction(area=area, mu=mu, sigma=sigma)
                yFitP += peakFunction(xFit)

            axScatter.plot(xFit, yFitP, label='Fit %s' % (peak_family_label))

        axScatter.set_xlim(xRoi[0], xRoi[-1])
        axScatter.set_xticks([])

        axScatter.legend(loc='best')

        residual = yRoi - yFit
        axHistx = figure.add_axes(rectA_residual)
        axHistx.plot(xFit, residual, label='Residual')
        axHistx.set_xlim(xRoi[0], xRoi[-1])
        axHistx.locator_params(axis='y', tight=True, nbins=4)

        basefilepath, _extension = os.path.splitext(self._spectrumFilepath)
        _path, basename = os.path.split(basefilepath)
        basefilepath = os.path.join(self._outputPath, basename)
        roiFitFigureFilepath = basefilepath + '_' + roiLabel.replace(" ", '_')
        for extension in ['.png']:
            figure.savefig(roiFitFigureFilepath+extension)

        if self.exportRois:
            saveFigureData(roiFitFigureFilepath+".csv")

        plt.clf()
        plt.close()
        del figure

        peakIntensities = []
        for peak_family_label in peak_family_list:
            family_height = result.params[peak_family_label+"_height"]
            family_position_keV = result.params[peak_family_label+"_position"]

            family_positionRef_keV = None
            for position_keV, fraction, label in peak_family_list[peak_family_label]:
                if label.endswith('a1') or peak_family_label == 'n':
                    family_positionRef_keV = position_keV

            delta_position = family_positionRef_keV - family_position_keV
            for position_keV, fraction, label in peak_family_list[peak_family_label]:
                mu = position_keV - delta_position
                sigma_keV = self._detector.getSigma_keV(position_keV)
                area = family_height*fraction*sigma*np.sqrt(2.0 * np.pi)
                yFitP = GaussianFunction(area=area, mu=mu, sigma=sigma_keV)(xFit)

                if not no_background:
                    yBackground = functionBackground(result.params, xFit)
                else:
                    yBackground = np.zeros_like(xFit)

                peakIntensity = PeakIntensity(xFit, yFitP, yBackground, mu, sigma_keV, label)
                peakIntensities.append(peakIntensity)

        return peakIntensities

    def _get_peak_family_list(self, roiPeaks):
        peak_family_list = {}
        for position_keV, fraction, label in roiPeaks:
            peak_family_label = label[:4].replace(' ', '_')
            peak_family_list.setdefault(peak_family_label, []).append([position_keV, fraction, label])

        return peak_family_list

    def _fitRoiPeaks(self, xRoi, yRoi, roiPeaks, roiLabel):
        from lmfit import minimize, Parameters

        parameters = Parameters()

        aGuess, bGuess = self._computeLinearBackgroundGuess(xRoi, yRoi)
        parameters.add('lb_a', value=aGuess, vary=True)
        parameters.add('lb_b', value=bGuess, vary=True)

        parameters.add('detector_Dn', value=40.0, min=0.0)
        parameters.add('detector_F', value=0.12, vary=False, min=0.0)

        positionRef_keV, fraction, label = roiPeaks[0]
        parameters.add('position', value=positionRef_keV)

        roiMax = np.max(yRoi)

        for position_keV, fraction, label in roiPeaks:
            electronicNoise_eV = parameters['detector_Dn'].value
            FanoFactor = parameters['detector_F'].value
            detector = DetectorFunction(electronicNoise_eV, FanoFactor)
            sigmaGuess = detector.getSigma_keV(position_keV)

            areaGuess = roiMax*fraction*sigmaGuess*np.sqrt(2.0 * np.pi)
            key = "%s_%s" % (label.replace(' ', '_'), "area")
            parameters.add(key, value=areaGuess, min=0.0)

        def functionBackground(parameters, x):
            a = parameters['lb_a'].value
            b = parameters['lb_b'].value
            linearBackground = PolynomialFirstDegreeFunction(a=a, b=b)

            return linearBackground(x)

        def peakFunction(parameters, x, baseKey, difference_keV):
            key = "%s_%s" % (baseKey, "area")
            area = parameters[key].value

            mu = parameters["position"].value + difference_keV

            electronicNoise_eV = parameters['detector_Dn'].value
            FanoFactor = parameters['detector_F'].value
            detector = DetectorFunction(electronicNoise_eV, FanoFactor)
            sigma = detector.getSigma_keV(mu)

            peakFunction = GaussianFunction(area=area, mu=mu, sigma=sigma)

            return peakFunction(x)

        def functionModel(parameters, x):
            model = functionBackground(parameters, x)

            for position_keV, fraction, label in roiPeaks:
                difference_keV = positionRef_keV - position_keV
                baseKey = label.replace(' ', '_')
                model += peakFunction(parameters, x, baseKey, difference_keV)

            return model

        def residual(parameters, x, data):
            model = functionModel(parameters, x)
            return (data-model)

        result  = minimize(residual, parameters, args=(xRoi, yRoi))

        #result  = minimize(residual, parameters, args=(xRoi, yRoi))

        xFit = xRoi
        yFit = functionModel(parameters, xFit)

        #logging.info("Fit succes?: %s", result.success)
        #logging.info("Number evaluation: %i", result.nfev)
        #logging.info("Message: %s", result.message)
        #logging.info("Residual: %s", calculateR2(yRoi, yFit) )
        #logging.info("chi2: %s", result.chisqr)
        #logging.info("reduced chi2: %s", result.redchi)

        logging.info('Best-Fit Values:')
        for name, par in parameters.items():
            logging.info('  %s = %.4f +/- %.4f', name, par.value, par.stderr)

        peakIntensities = []

        left= 0.1
        width = 1.0 - 2.0 * left

        bottom_h = 0.1
        height_h = 0.1
        bottom = bottom_h + height_h + 0.02
        height = 1.0 - bottom - 0.1

        assert (left + width) <= 1.0
        assert (bottom + height) <= 1.0

        rectA_profile = [left, bottom, width, height]
        rectA_residual = [left, bottom_h, width, height_h]

        figure = plt.figure()
        #figure.clf()
        figure.suptitle(roiLabel, fontsize=16)
        axScatter = figure.add_axes(rectA_profile)

        axScatter.plot(xRoi, yRoi, '.', label='Data')
        axScatter.plot(xFit, yFit, label='Fit')

        yFitLB = functionBackground(parameters, xFit)
        axScatter.plot(xFit, yFitLB, label='Fit LB')

        for position_keV, fraction, label in roiPeaks:
            difference_keV = positionRef_keV - position_keV
            baseKey = label.replace(' ', '_')
            yFitP = peakFunction(parameters, xFit, baseKey, difference_keV)
            axScatter.plot(xFit, yFitP, label='Fit %s' % (label))


        axScatter.set_xlim(xRoi[0], xRoi[-1])
        axScatter.set_xticks([])

        axScatter.legend(loc='best')

        residual = yRoi - yFit
        axHistx = figure.add_axes(rectA_residual)
        axHistx.plot(xFit, residual, label='Residual')
        axHistx.set_xlim(xRoi[0], xRoi[-1])
        axHistx.locator_params(axis='y', tight=True, nbins=4)

        basefilepath, _extension = os.path.splitext(self._spectrumFilepath)
        _path, basename = os.path.split(basefilepath)
        basefilepath = os.path.join(self._outputPath, basename)
        roiFitFigureFilepath = basefilepath + '_' + roiLabel.replace(" ", '_')
        for extension in ['.png']:
            figure.savefig(roiFitFigureFilepath+extension)

        plt.clf()
        plt.close()
        del figure

        return peakIntensities

    def _computeLinearBackgroundGuess(self, xRoi, yRoi):
        x1 = xRoi[0]
        x2 = xRoi[-1]
        y1 = yRoi[0]
        y2 = yRoi[-1]

        bGuess = (y2 - y1)/(x2 - x1)
        aGuess = y1 - bGuess*x1

        return aGuess, bGuess

    def savePeakIntensities(self, peakIntensities):
        spectrumFilename = os.path.basename(self._spectrumFilepath)
        filename, _extension = os.path.splitext(spectrumFilename)
        intensitiesFilepath = os.path.join(self._outputPath, filename+'.csv')
        writer = csv.writer(open(intensitiesFilepath, 'w', newline='\n'))

        rowHeader = ["Line", "Counts", "Background", "Position (keV)", "FWHM (eV)", "Counts (1.2*FWHM)", "Background (1.2*FWHM)"]
        writer.writerow(rowHeader)

        for peakIntensity in peakIntensities:
            optimumWidth_keV = 1.2 * peakIntensity.fwhm_keV
            row = []
            row.append(peakIntensity.label)
            row.append(peakIntensity.counts)
            row.append(peakIntensity.countsBackground)
            row.append(peakIntensity.position_keV)
            row.append(peakIntensity.fwhm_eV)
            row.append(peakIntensity.countsFromFixedWidth(optimumWidth_keV))
            row.append(peakIntensity.countsBackgroundFromFixedWidth(optimumWidth_keV))
            writer.writerow(row)

    def setDetector(self, electronicNoise_eV, FanoFactor):
        self._detector = DetectorFunction(electronicNoise_eV, FanoFactor)

    @property
    def showEdgeMarkers(self):
        return self._showEdgeMarkers
    @showEdgeMarkers.setter
    def showEdgeMarkers(self, showEdgeMarkers):
        self._showEdgeMarkers = showEdgeMarkers

    @property
    def showMajorLineMarkers(self):
        return self._showMajorLineMarkers
    @showMajorLineMarkers.setter
    def showMajorLineMarkers(self, showMajorLineMarkers):
        self._showMajorLineMarkers = showMajorLineMarkers

    @property
    def showMinorLineMarkers(self):
        return self._showMinorLineMarkers
    @showMinorLineMarkers.setter
    def showMinorLineMarkers(self, showMinorLineMarkers):
        self._showMinorLineMarkers = showMinorLineMarkers

    @property
    def showSatelliteLineMarkers(self):
        return self._showSatelliteLineMarkers
    @showSatelliteLineMarkers.setter
    def showSatelliteLineMarkers(self, showSatelliteLineMarkers):
        self._showSatelliteLineMarkers = showSatelliteLineMarkers

    @property
    def showSiEscapeMarkers(self):
        return self._showSiEscapeMarkers
    @showSiEscapeMarkers.setter
    def showSiEscapeMarkers(self, showSiEscapeMarkers):
        self._showSiEscapeMarkers = showSiEscapeMarkers

    @property
    def showRois(self):
        return self._showRois
    @showRois.setter
    def showRois(self, showRois):
        self._showRois = showRois

    @property
    def showFittedPeaks(self):
        return self._showFittedPeaks
    @showFittedPeaks.setter
    def showFittedPeaks(self, showFittedPeaks):
        self._showFittedPeaks = showFittedPeaks

    @property
    def exportRois(self):
        return self._exportRois
    @exportRois.setter
    def exportRois(self, exportRois):
        self._exportRois = exportRois

    @property
    def fitMethod(self):
        return self._fitMethod
    @fitMethod.setter
    def fitMethod(self, fitMethod):
        self._fitMethod = fitMethod

    @property
    def hasDoubleCarbonPeak(self):
        return self._hasDoubleCarbonPeak
    @hasDoubleCarbonPeak.setter
    def hasDoubleCarbonPeak(self, hasDoubleCarbonPeak):
        self._hasDoubleCarbonPeak = hasDoubleCarbonPeak

    @property
    def maximumEnergy_keV(self):
        return self._maximumEnergy_keV
    @maximumEnergy_keV.setter
    def maximumEnergy_keV(self, maximumEnergy_keV):
        self._maximumEnergy_keV = maximumEnergy_keV

def showGraphics():
    logging.info("Display graphics")
    plt.show()

def run():
    currentPath = get_current_module_path(__file__)
    configurationFilepath = os.path.join(currentPath, "../SpectrumAnalyzer.cfg")

    outputPath = os.path.join(currentPath, "../testData/tmp/RareEarth_20120307_SiO2")
    spectrumFilepath = os.path.join(currentPath, "../testData/OxfordInstruments/RareEarth_20120307_SiO2.txt")

    spectrumAnalyzer = SpectrumAnalyzer(outputPath=outputPath, configurationFilepath=configurationFilepath)

    spectrumAnalyzer.addElement("Si")
    spectrumAnalyzer.addElement("O")

    spectrumAnalyzer.addRoi("Roi 1", (0.3, 0.8))
    spectrumAnalyzer.addRoi("Roi 2", (1.4, 2.0))

    spectrumAnalyzer.analyze(spectrumFilepath)
    spectrumAnalyzer.showGraphic()

if __name__ == '__main__': #pragma: no cover
    run()
