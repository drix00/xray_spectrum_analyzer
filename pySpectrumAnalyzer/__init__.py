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
import os.path
import logging

# Third party modules.
import matplotlib
import matplotlib.pyplot as plt
import numpy
import matplotlib.mlab as mlab

# Local modules.

# Globals and constants variables.


def createPath(path):
    """
    Create a path from the input string if does not exists.

    Does not try to distinct between file and directory in the input string.
    path = "dir1/filename.ext" => "dir1/filename.ext/"
    where the new directory "filename.ext" is created.

    @param[in] path input string.

    @return the path with the path separator at the end.

    """
    path = os.path.normpath(path)
    if not os.path.exists(path):
        os.makedirs(path)

    if len(path) > 0 and path[-1] != os.sep:
        path += os.sep

    return path


def get_current_module_path(modulePath, relativePath=""):
    basepath = os.path.dirname(modulePath)
    #logging.debug(basepath)

    filepath = os.path.join(basepath, relativePath)
    #logging.debug(filepath)
    filepath = os.path.normpath(filepath)

    return filepath


def saveFigureData(filepath, figure=None):
    if figure is None:
        figure = plt.gcf()

    axes = figure.get_axes()

    #label = figure.get_label()
    #print "Figure label:", label

    for iAxe, axe in enumerate(axes):
        lines = axe.get_lines()

        axeLabel = axe.get_label()
        if len(axeLabel) == 0 and len(axes) > 1:
            axeLabel = 'axe%i' % iAxe

        for iLine,line in enumerate(lines):
            logging.debug(line)
            if isinstance(line, matplotlib.lines.Line2D):
                saveLineData(filepath, line, iLine, axeLabel)


def saveLineData(filepath, line, iLine, axeLabel="", label=None, xLabel=None, yLabel=None):
    if label is None:
        label = line.get_label()
    else:
        if len(label) == 0:
            label = 'line%i' % iLine

    if label[0] != '_':
        label = "_" + label

    if xLabel is None:
        xLabel = line.get_axes().get_xaxis().get_label().get_text()

    if yLabel is None:
        yLabel = line.get_axes().get_yaxis().get_label().get_text()

    if len(xLabel) == 0:
        xLabel = 'X'

    if len(yLabel) == 0:
        yLabel = 'Y'

    #print label, xLabel, yLabel

    xData = line.get_xdata()
    yData = line.get_ydata()

    names = xLabel + "," + yLabel

    recordData = numpy.rec.fromarrays([xData, yData], names=names)

    filepath = os.path.splitext(filepath)[0]
    if len(axeLabel) > 0:
        filepath += "_" + axeLabel

    filepath += label

    saveDataRecord(recordData, filepath, hasExtension=False)


def saveDataRecord(recordData, filepath, hasExtension=True):
    if hasExtension:
        filepath, dummyExtention = os.path.splitext(filepath)
    filepath += ".csv"

    createPath(os.path.dirname(filepath))

    mlab.rec2csv(recordData, filepath)
