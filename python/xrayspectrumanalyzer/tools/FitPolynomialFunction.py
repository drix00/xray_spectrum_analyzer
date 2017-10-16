#!/usr/bin/env python
"""
.. py:currentmodule:: ProbeBroadening3D.fit.FitPolynomialFunction
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

description
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
import numpy as np

# Local modules.

# Project modules
import xrayspectrumanalyzer.tools.fitTools as fitTools

# Globals and constants variables.

class FitPolynomialFirstDegreeFunction(fitTools._FitObject):
    def __init__(self, a=None, b=None):
        if a is None:
            self._aFixed = False
        else:
            self._aFixed = True
        self._a = a

        if b is None:
            self._bFixed = False
        else:
            self._bFixed = True
        self._b = b

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._aFixed:
            self._a = parameters[indexParameters]
            indexParameters +=1

        if not self._bFixed:
            self._b = parameters[indexParameters]
            indexParameters +=1

        yFit = self.function(x)
        return yFit

    def function(self, x):
        return self._a + self._b*x

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._aFixed:
            numberParameters +=1
        if not  self._bFixed:
            numberParameters +=1

        return numberParameters

class FitPolynomialSecondDegreeFunction(fitTools._FitObject):
    def __init__(self, a=None, b=None, c=None):
        if a is None:
            self._aFixed = False
        else:
            self._aFixed = True
        self._a = a

        if b is None:
            self._bFixed = False
        else:
            self._bFixed = True
        self._b = b

        if c is None:
            self._cFixed = False
        else:
            self._cFixed = True
        self._c = c

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._aFixed:
            self._a = parameters[indexParameters]
            indexParameters +=1

        if not self._bFixed:
            self._b = parameters[indexParameters]
            indexParameters +=1

        if not self._cFixed:
            self._c = parameters[indexParameters]
            indexParameters +=1

        yFit = self.function(x)
        return yFit

    def function(self, x):
        return self._a + self._b*x + self._c*np.power(x, 2.0)

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._aFixed:
            numberParameters +=1
        if not self._bFixed:
            numberParameters +=1
        if not self._cFixed:
            numberParameters +=1

        return numberParameters

class FitPolynomialThirdDegreeFunction(fitTools._FitObject):
    def __init__(self, a=None, b=None, c=None, d=None):
        if a is None:
            self._aFixed = False
        else:
            self._aFixed = True
        self._a = a

        if b is None:
            self._bFixed = False
        else:
            self._bFixed = True
        self._b = b

        if c is None:
            self._cFixed = False
        else:
            self._cFixed = True
        self._c = c

        if d is None:
            self._dFixed = False
        else:
            self._dFixed = True
        self._d = d

    def evaluation(self, x, parameters):
        indexParameters = 0

        if not self._aFixed:
            self._a = parameters[indexParameters]
            indexParameters +=1

        if not self._bFixed:
            self._b = parameters[indexParameters]
            indexParameters +=1

        if not self._cFixed:
            self._c = parameters[indexParameters]
            indexParameters +=1

        if not self._dFixed:
            self._d = parameters[indexParameters]
            indexParameters +=1

        yFit = self.function(x)
        return yFit

    def function(self, x):
        return self._a + self._b*x + self._c*np.power(x, 2.0) + self._d*np.power(x, 3.0)

    def getNumberFitParameters(self):
        numberParameters = 0
        if not self._aFixed:
            numberParameters +=1
        if not self._bFixed:
            numberParameters +=1
        if not self._cFixed:
            numberParameters +=1
        if not self._dFixed:
            numberParameters +=1

        return numberParameters

class PolynomialFirstDegreeFunction(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def __call__(self, x):
        return self._a + self._b*x

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
