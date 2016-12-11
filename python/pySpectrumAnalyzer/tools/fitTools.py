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

# Globals and constants variables.

class _FitObject(object):
    def residual(self, parameters, y, x):
        yFit = self.evaluation(x, parameters)
        error = y - yFit

        return error

    def residualLog(self, parameters, y, x):
        yFit = self.evaluation(x, parameters)
        error = np.log(y) - np.log(yFit)

        return error

    def evaluation(self, x, parameters):
        raise NotImplementedError

    def function(self, x):
        raise NotImplementedError

    def getNumberFitParameters(self):
        raise NotImplementedError

class FitFunctions(_FitObject):
    def __init__(self, fitFunctions):
        self._setupFitFunction(fitFunctions)

    def _setupFitFunction(self, fitFunctions):
        self._fitFunctions = {}

        iStart = 0
        iEnd = 0
        for index, fitFunction in enumerate(fitFunctions):
            numberParameters = fitFunction.getNumberFitParameters()
            iEnd += numberParameters
            self._fitFunctions[index] = (fitFunction, iStart, iEnd)
            iStart = iEnd

    def evaluation(self, x, parameters):
        yFit = 0.0

        for fitFunctionName in self._fitFunctions:
            fitFunction, iStart, iEnd = self._fitFunctions[fitFunctionName]
            parametersFunction = parameters[iStart:iEnd]
            yFit += fitFunction.evaluation(x, parametersFunction)

        return yFit

    def function(self, x):
        y = 0.0

        for fitFunctionName in self._fitFunctions:
            fitFunction, iStart, iEnd = self._fitFunctions[fitFunctionName]
            y += fitFunction.function(x)

        return y

    def getNumberFitParameters(self):
        numberParameters = 0
        for fitFunctionName in self._fitFunctions:
            fitFunction, dummy_iStart, dummy_iEnd = self._fitFunctions[fitFunctionName]
            numberParameters += fitFunction.getNumberFitParameters()

        return numberParameters

def calculateR2(ys, fitYs):
    SSE = 0.0
    SSR = 0.0
    ybar = np.mean(ys)
    for i, fitY in enumerate(fitYs):
        SSE += (ys[i] - fitY) ** 2
        SSR += (fitY - ybar) ** 2

    return SSR / (SSE + SSR)

if __name__ == '__main__':  #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
