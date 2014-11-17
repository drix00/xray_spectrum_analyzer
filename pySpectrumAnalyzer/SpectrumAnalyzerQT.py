#!/usr/bin/env python

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2292 $"
__svnDate__ = "$Date: 2011-03-21 11:29:50 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: SpectrumAnalyzerQT.py 2292 2011-03-21 15:29:50Z hdemers $"

import sys

from PyQt4 import Qt, QtGui
from ui_viewer import Ui_Form

from PyQt4.Qwt5 import Qwt

class ImageDialog(QtGui.QWidget, Ui_Form):
    def __init__(self, filename=None):
        QtGui.QWidget.__init__(self)

        Ui_Form.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)

        self.picker = None

        self.zoomer = None

        self.energyList = []
        self.intensityList = []

        # curves
        self.qwtPlot_viewer.curve1 = Qwt.QwtPlotCurve('Spectrum')
        self.qwtPlot_viewer.curve1.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        self.qwtPlot_viewer.curve1.setPen(Qt.QPen(Qt.Qt.red))
        self.qwtPlot_viewer.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        self.qwtPlot_viewer.curve1.attach(self.qwtPlot_viewer)

        if filename:
            self.readData(filename)
            self.showData(self.energyList, self.intensityList)

        self.createZoomer()
        self.createPicker()

    def createPicker(self):
        self.picker = Qwt.QwtPlotPicker(Qwt.QwtPlot.xBottom,
                                                             Qwt.QwtPlot.yLeft,
                                                             Qwt.QwtPicker.NoSelection,
                                                             Qwt.QwtPlotPicker.CrossRubberBand,
                                                             Qwt.QwtPicker.AlwaysOn,
                                                             self.qwtPlot_viewer.canvas())
        self.picker.setTrackerPen(Qt.QPen(Qt.Qt.blue))

    def createZoomer(self):
        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                                             Qwt.QwtPlot.yLeft,
                                                             Qwt.QwtPicker.DragSelection,
                                                             Qwt.QwtPicker.AlwaysOff,
                                                             self.qwtPlot_viewer.canvas())
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

    def readData(self, filename):
        self.energyList = []
        self.intensityList = []

        for line in open(filename, 'r').readlines():
            if len(line) > 0 and line[0] != '#':
                energy, intensity = line.split(',')
                self.energyList.append(float(energy))
                self.intensityList.append(float(intensity))

        print len(self.energyList), len(self.intensityList)

    def showData(self, energy, intensity):
        self.qwtPlot_viewer.curve1.setData(energy, intensity)

def run():
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv) == 2:
        window = ImageDialog(sys.argv[1])
    else:
        window = ImageDialog("inputData/Spectrum 2.txt")

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
