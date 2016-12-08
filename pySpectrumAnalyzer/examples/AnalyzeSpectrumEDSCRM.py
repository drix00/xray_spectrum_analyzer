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
import logging
import os.path

import pyHendrixDemersTools.Files as Files

import pySpectrumAnalyzer.examples.ComputePeaksIntensities as ComputePeaksIntensities

# Globals and constants variables.
CKA = "C Ka"
MNLA = "Mn La1"
CULA = "Cu La1"
ALKA = "Al Ka"
ZRL = "Zr L"
MNKA = "Mn Ka"
CUKA = "Cu Ka"
ZRKA = "Zr Ka"
ZRKB = "Zr Kb"

def runLeo080530_10keV_s02():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080530/myFit/10keV/")

    spectrumFilename = "spectrum02.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(CKA)
    computePeaksIntensities.setPeakRange(CKA, 0.16, 0.356)
    computePeaksIntensities.setPosition_keV(CKA, 0.268)

    computePeaksIntensities.addPeak(MNLA)
    computePeaksIntensities.setPeakRange(MNLA, 0.566, 0.743)
    computePeaksIntensities.setPosition_keV(MNLA, 0.63)

    computePeaksIntensities.addPeak(CULA)
    computePeaksIntensities.setPeakRange(CULA, 0.82, 1.10)
    computePeaksIntensities.setPosition_keV(CULA, 0.924)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.3, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.2)
    computePeaksIntensities.setPosition_keV(MNKA, 5.82)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080530_10keV_s05():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080530/myFit/10keV/")

    spectrumFilename = "spectrum05.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(CKA)
    computePeaksIntensities.setPeakRange(CKA, 0.16, 0.356)
    computePeaksIntensities.setPosition_keV(CKA, 0.268)

    computePeaksIntensities.addPeak(MNLA)
    computePeaksIntensities.setPeakRange(MNLA, 0.566, 0.743)
    computePeaksIntensities.setPosition_keV(MNLA, 0.63)

    computePeaksIntensities.addPeak(CULA)
    computePeaksIntensities.setPeakRange(CULA, 0.82, 1.10)
    computePeaksIntensities.setPosition_keV(CULA, 0.924)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.3, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.2)
    computePeaksIntensities.setPosition_keV(MNKA, 5.82)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080530_30keV_s08():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080530/myFit/30keV/")

    spectrumFilename = "spectrum08.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.35, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.1)
    computePeaksIntensities.setPosition_keV(MNKA, 5.83)

    computePeaksIntensities.addPeak(CUKA)
    computePeaksIntensities.setPeakRange(CUKA, 7.6, 8.4)
    computePeaksIntensities.setPosition_keV(CUKA, 7.94)

    computePeaksIntensities.addPeak(ZRKA)
    computePeaksIntensities.setPeakRange(ZRKA, 15.0, 16.2)
    computePeaksIntensities.setPosition_keV(ZRKA, 15.5)

    computePeaksIntensities.addPeak(ZRKB)
    computePeaksIntensities.setPeakRange(ZRKB, 16.8, 18.3)
    computePeaksIntensities.setPosition_keV(ZRKB, 17.4)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080530_30keV_s11():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080530/myFit/30keV/")

    spectrumFilename = "spectrum11.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.35, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.1)
    computePeaksIntensities.setPosition_keV(MNKA, 5.83)

    computePeaksIntensities.addPeak(CUKA)
    computePeaksIntensities.setPeakRange(CUKA, 7.6, 8.4)
    computePeaksIntensities.setPosition_keV(CUKA, 7.94)

    computePeaksIntensities.addPeak(ZRKA)
    computePeaksIntensities.setPeakRange(ZRKA, 15.0, 16.2)
    computePeaksIntensities.setPosition_keV(ZRKA, 15.5)

    computePeaksIntensities.addPeak(ZRKB)
    computePeaksIntensities.setPeakRange(ZRKB, 16.8, 18.3)
    computePeaksIntensities.setPosition_keV(ZRKB, 17.4)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080611_10keV_s02():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080611/myFit/10keV/")

    spectrumFilename = "s02.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(CKA)
    computePeaksIntensities.setPeakRange(CKA, 0.16, 0.356)
    computePeaksIntensities.setPosition_keV(CKA, 0.268)

    computePeaksIntensities.addPeak(MNLA)
    computePeaksIntensities.setPeakRange(MNLA, 0.566, 0.743)
    computePeaksIntensities.setPosition_keV(MNLA, 0.63)

    computePeaksIntensities.addPeak(CULA)
    computePeaksIntensities.setPeakRange(CULA, 0.82, 1.10)
    computePeaksIntensities.setPosition_keV(CULA, 0.924)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.3, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.2)
    computePeaksIntensities.setPosition_keV(MNKA, 5.82)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080611_10keV_s05():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080611/myFit/10keV/")

    spectrumFilename = "s05.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(CKA)
    computePeaksIntensities.setPeakRange(CKA, 0.16, 0.356)
    computePeaksIntensities.setPosition_keV(CKA, 0.268)

    computePeaksIntensities.addPeak(MNLA)
    computePeaksIntensities.setPeakRange(MNLA, 0.566, 0.743)
    computePeaksIntensities.setPosition_keV(MNLA, 0.63)

    computePeaksIntensities.addPeak(CULA)
    computePeaksIntensities.setPeakRange(CULA, 0.82, 1.10)
    computePeaksIntensities.setPosition_keV(CULA, 0.924)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.3, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.2)
    computePeaksIntensities.setPosition_keV(MNKA, 5.82)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080611_30keV_s08():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080611/myFit/30keV/")

    spectrumFilename = "s08.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.35, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.1)
    computePeaksIntensities.setPosition_keV(MNKA, 5.83)

    computePeaksIntensities.addPeak(CUKA)
    computePeaksIntensities.setPeakRange(CUKA, 7.6, 8.4)
    computePeaksIntensities.setPosition_keV(CUKA, 7.94)

    computePeaksIntensities.addPeak(ZRKA)
    computePeaksIntensities.setPeakRange(ZRKA, 15.0, 16.2)
    computePeaksIntensities.setPosition_keV(ZRKA, 15.5)

    computePeaksIntensities.addPeak(ZRKB)
    computePeaksIntensities.setPeakRange(ZRKB, 16.8, 18.3)
    computePeaksIntensities.setPosition_keV(ZRKB, 17.4)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runLeo080611_30keV_s11():
    basepath = Files.getCnseResultsPath("SpectrumAnalyzer.cfg", "SEM/LEO1550/080611/myFit/30keV/")

    spectrumFilename = "s11.emsa"

    logging.info("Analyzing spectrum file %s.", spectrumFilename)

    filepath = os.path.join(basepath, spectrumFilename)
    computePeaksIntensities = ComputePeaksIntensities.ComputePeaksIntensities(filepath)

    computePeaksIntensities.addPeak(ALKA)
    computePeaksIntensities.setPeakRange(ALKA, 1.35, 1.62)
    computePeaksIntensities.setPosition_keV(ALKA, 1.47)

    computePeaksIntensities.addPeak(ZRL)
    computePeaksIntensities.setPeakRange(ZRL, 1.86, 2.4)
    computePeaksIntensities.setPosition_keV(ZRL, 2.03)

    computePeaksIntensities.addPeak(MNKA)
    computePeaksIntensities.setPeakRange(MNKA, 5.4, 6.1)
    computePeaksIntensities.setPosition_keV(MNKA, 5.83)

    computePeaksIntensities.addPeak(CUKA)
    computePeaksIntensities.setPeakRange(CUKA, 7.6, 8.4)
    computePeaksIntensities.setPosition_keV(CUKA, 7.94)

    computePeaksIntensities.addPeak(ZRKA)
    computePeaksIntensities.setPeakRange(ZRKA, 15.0, 16.2)
    computePeaksIntensities.setPosition_keV(ZRKA, 15.5)

    computePeaksIntensities.addPeak(ZRKB)
    computePeaksIntensities.setPeakRange(ZRKB, 16.8, 18.3)
    computePeaksIntensities.setPosition_keV(ZRKB, 17.4)

    computePeaksIntensities.fitAllPeaks()
    computePeaksIntensities.printRestults()

    computePeaksIntensities.saveRestults()

    return computePeaksIntensities

def runAll():

    runLeo080611_10keV_s02()

    runLeo080611_10keV_s05()

    runLeo080611_30keV_s08()

    runLeo080611_30keV_s11()

    runLeo080530_10keV_s02()

    runLeo080530_10keV_s05()

    runLeo080530_30keV_s08()

    runLeo080530_30keV_s11()


if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=runAll)
