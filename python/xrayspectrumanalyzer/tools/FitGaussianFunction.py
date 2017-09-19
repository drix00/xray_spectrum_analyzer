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

# Third party modules.
import numpy as np

# Local modules.

# Project modules
import pySpectrumAnalyzer.tools.fitTools as fitTools

# Globals and constants variables.

class FitGaussianFunction(fitTools._FitObject):
    def __init__(self, area=None, mu=None, sigma=None):
        if area is None:
            self._areaFixed = False
        else:
            self._areaFixed = True
        self._area = area

        if mu is None:
            self._muFixed = False
        else:
            self._muFixed = True
        self._mu = mu

        if sigma is None:
            self._sigmaFixed = False
        else:
            self._sigmaFixed = True
        self._sigma = sigma

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._areaFixed:
            self._area = parameters[indexParameters]
            indexParameters +=1

        if not self._muFixed:
            self._mu = parameters[indexParameters]
            indexParameters +=1

        if not self._sigmaFixed:
            self._sigma = parameters[indexParameters]
            indexParameters +=1

        yFit = self.function(x)
        return yFit

    def function(self, x):
        return self._area*1.0/(self._sigma*np.sqrt(2.0*np.pi)) * np.exp((-(x - self._mu)**2)/(2.0*self._sigma**2))

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._areaFixed:
            numberParameters +=1
        if not  self._muFixed:
            numberParameters +=1
        if not  self._sigmaFixed:
            numberParameters +=1

        return numberParameters

class FitGaussianWithYFunction(FitGaussianFunction):
    def __init__(self, area=None, mu=None, sigma=None, y0=None):
        if area is None:
            self._areaFixed = False
        else:
            self._areaFixed = True
        self._area = area

        if mu is None:
            self._muFixed = False
        else:
            self._muFixed = True
        self._mu = mu

        if sigma is None:
            self._sigmaFixed = False
        else:
            self._sigmaFixed = True
        self._sigma = sigma

        if y0 is None:
            self._y0Fixed = False
        else:
            self._y0Fixed = True
        self._y0 = y0

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._areaFixed:
            self._area = parameters[indexParameters]
            indexParameters +=1

        if not self._muFixed:
            self._mu = parameters[indexParameters]
            indexParameters +=1

        if not self._sigmaFixed:
            self._sigma = parameters[indexParameters]
            indexParameters +=1

        if not self._y0Fixed:
            self._y0 = parameters[indexParameters]
            indexParameters +=1

        yFit = self._y0 + self._area*1.0/(self._sigma*np.sqrt(2.0*np.pi)) * np.exp((-(x - self._mu)**2)/(2.0*self._sigma**2))
        return yFit

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._areaFixed:
            numberParameters +=1
        if not  self._muFixed:
            numberParameters +=1
        if not  self._sigmaFixed:
            numberParameters +=1
        if not self._y0Fixed:
            numberParameters +=1

        return numberParameters

class GaussianFunction(object):
    def __init__(self, area, mu, sigma):
        self._area = area
        self._mu = mu
        self._sigma = sigma

    def __call__(self, x):
        return self._area*1.0/(self._sigma*np.sqrt(2.0*np.pi)) * np.exp((-(x - self._mu)**2)/(2.0*self._sigma**2))

if __name__ == '__main__':  #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
