#!/usr/bin/env python
"""
.. py:currentmodule:: xrayGenerator
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Generate x-ray from a specific input count rate.
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

# Third party modules.
import matplotlib.pyplot as plt
import numpy as np

# Local modules.

# Project modules

# Globals and constants variables.

class XrayGenerator(object):
    def __init__(self):
        self.numberXrays = 1000000
        self.countRate_cps = 100.0e3

        self.processingTime_us = 10.0

    def computeMethod1(self):
        timeIntervals_s = np.random.poisson(self._countRate_cps, self._numberXrays)

        plt.figure()
        plt.title("Method 1")
        plt.hist(timeIntervals_s, bins=20)

    def computeMethod2(self):
        timeIntervals_s = self._computeTimeIntervals_s()

        plt.figure()
        plt.title("Method 2")
        plt.hist(timeIntervals_s, bins=20)

    def _computeTimeIntervals_s(self):
        randomNumbers_s = np.random.random(self._numberXrays)
        timeIntervals_s = -1.0 * np.log(1.0 - randomNumbers_s) / self._countRate_cps

        return timeIntervals_s

    def computeDeadTime(self):
        timeIntervals_s = self._computeTimeIntervals_s()

        processingTime_s = self._processingTime_us*1.0e-6
        outputCounts = np.ma.masked_less(timeIntervals_s, processingTime_s).count()

        deadTimeFraction = 1.0 - float(outputCounts)/float(self._numberXrays)

        return deadTimeFraction

    @property
    def numberXrays(self):
        return self._numberXrays
    @numberXrays.setter
    def numberXrays(self, numberXrays):
        self._numberXrays = numberXrays

    @property
    def countRate_cps(self):
        return self._countRate_cps
    @countRate_cps.setter
    def countRate_cps(self, countRate_cps):
        self._countRate_cps = countRate_cps

    @property
    def processingTime_us(self):
        return self._processingTime_us
    @processingTime_us.setter
    def processingTime_us(self, processingTime_us):
        self._processingTime_us = processingTime_us

def run():
    xrayGenerator = XrayGenerator()

    #xrayGenerator.computeMethod1()
    #xrayGenerator.computeMethod2()

    xrayGenerator.numberXrays = 1000000
    xrayGenerator.processingTime_us = 10.0

    #countRates_cps = np.arange(1.0, 1.0e6, 100.0)
    countRates_cps = [1.0, 10.0, 1.0e2, 1.03, 1.0e4, 1.0e5, 1.0e6]

    deadTimeFractions = []
    for countRate_cps in countRates_cps:
        xrayGenerator.countRate_cps = countRate_cps
        deadTimeFraction = xrayGenerator.computeDeadTime()
        deadTimeFractions.append(deadTimeFraction)

    plt.figure()

    plt.semilogx(countRates_cps, deadTimeFractions)

    plt.show()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
