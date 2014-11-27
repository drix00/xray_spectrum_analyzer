#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2937 $"
__svnDate__ = "$Date: 2014-09-01 10:20:37 -0400 (Mon, 01 Sep 2014) $"
__svnId__ = "$Id: SpectrumAnalyzerGUI.py 2937 2014-09-01 14:20:37Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import pySpectrumAnalyzer.ui.gui.Tk.Options
import pySpectrumAnalyzer.ui.gui.Tk.MainWindow
import pySpectrumAnalyzer.SpectrumAnalyzerData as SpectrumAnalyzerData
import pySpectrumAnalyzer.SpectrumAnalyzerEngine as SpectrumAnalyzerEngine

# Globals and constants variables.

class SpectrumAnalyzerGUI(object):
    def __init__(self, args=None, configurationFile=None):
        self._options = pySpectrumAnalyzer.ui.gui.Tk.Options.Options(args, configurationFile)

        self._data = SpectrumAnalyzerData.SpectrumAnalyzerData()

        self._engine = SpectrumAnalyzerEngine.SpectrumAnalyzerEngine()

    def run(self):
        if self._options.getUI() == pySpectrumAnalyzer.ui.gui.Tk.Options.UI_TK:
            self._runTk()

    def _runTk(self):
        pySpectrumAnalyzer.ui.gui.Tk.MainWindow.run(self._options, self._data, self._engine)

# TODO: Read command line options.
# TODO: Read configuration files options.
# TODO: Read and save GUI options.

def run():
    saGUI = SpectrumAnalyzerGUI()

    saGUI.run()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
