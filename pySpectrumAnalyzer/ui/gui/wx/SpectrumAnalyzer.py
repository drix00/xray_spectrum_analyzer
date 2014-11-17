#!/usr/bin/env python
"""
.. py:currentmodule:: gui.SpectrumAnalyzer
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Main gui for Spectrum Analyzer application.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision$"
__svnDate__ = "$Date$"
__svnId__ = "$Id$"

# Standard library modules.
import os
import logging

# Third party modules.
import wx

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# Local modules.
#from wxtools.messagedialog import show_exception_dialog
#from wxtools.filedialog import FileDialog
import pySpectrumFileFormat.emmff.emsa as emsa

# Project modules
from ui.gui.wx import SpectrumViewer

# Globals and constants variables.
ID_SAVE_ALL = wx.NewId()

ART_MAP = {wx.ID_OPEN: wx.ART_FILE_OPEN,
           wx.ID_SAVE: wx.ART_FILE_SAVE,
           wx.ID_SAVEAS: wx.ART_FILE_SAVE_AS,
           ID_SAVE_ALL: wx.ART_FILE_SAVE,
           wx.ID_CLOSE: wx.ART_CROSS_MARK,
           wx.ID_CLOSE_ALL: wx.ART_CROSS_MARK,
           wx.ID_EXIT: wx.ART_CROSS_MARK}

class MainToolbar(wx.ToolBar):
    def add_tool(self, stockID, shortHelp="", longHelp=""):
        """
        Simplifies adding a tool to the toolbar.

        @param stockID: Stock ID
        @param shortHelp: short help text
        @param longHelp: long help text
        """
        assert stockID in ART_MAP, "Unknown stock ID."

        art_id = ART_MAP.get(stockID)

        bitmap = wx.ArtProvider.GetBitmap(art_id, wx.ART_TOOLBAR)
        self.AddSimpleTool(stockID, bitmap, shortHelpString=shortHelp, longHelpString=longHelp)

class SpectrumViewerPanel(wx.Panel):
    def __init__(self, parent, figure, figureSize):
        #figureSize = figure.get_size()
        #dpi = figure.dpi
        #frameSize = (int(figureSize[0]*dpi), int(figureSize[1]*dpi))
        super(SpectrumViewerPanel, self).__init__(parent, style=wx.TAB_TRAVERSAL|wx.BORDER)

        self._viewer = SpectrumViewer.SpectrumViewer(figure)

        self._canvas = FigureCanvas(self, wx.ID_ANY, figure)
        toolbar = SpectrumViewer.NavigationToolbar(self._canvas, self._viewer)

        figsizer = wx.BoxSizer(wx.VERTICAL)
        figsizer.Add(self._canvas, 1, wx.LEFT | wx.TOP)
        figsizer.Add(toolbar, 0, wx.LEFT | wx.TOP)

        self.SetSizer(figsizer)

class MainFrame(wx.Frame):

    def __init__(self, parent, title='Spectrum Analyzer'):
        logging.debug("Init MainFrame")

        wx.Frame.__init__(self, parent, wx.ID_ANY, title)

        #### Variables
        figureSize = (8, 6)
        self._figure = Figure(figureSize)

        self._spectrumViewerPanel = SpectrumViewerPanel(self, self._figure, figureSize)

        self._spectra = {}
        self._currentSpectrumKey = None

        #### Controls
        # Menu bar
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_OPEN, "&Open\tCtrl+O", "Open spectrum")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_SAVE, "Save\tCtrl+S")
        fileMenu.Append(wx.ID_SAVEAS, "Save As...")
        fileMenu.Append(ID_SAVE_ALL, "Save All\tCtrl+Shift+S")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_CLOSE, "Close\tCtrl+W")
        fileMenu.Append(wx.ID_CLOSE_ALL, "Close All\tCtrl+Shift+W")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT, "Exit")

        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        # Toolbar
        toolbar = MainToolbar(self)

        toolbar.add_tool(wx.ID_OPEN)
        toolbar.AddSeparator()
        toolbar.add_tool(wx.ID_SAVE)
        toolbar.add_tool(wx.ID_SAVEAS)
        #toolbar.add_tool(ID_SAVE_ALL)
        toolbar.AddSeparator()
        toolbar.add_tool(wx.ID_CLOSE)
        #toolbar.add_tool(wx.ID_CLOSE_ALL)

        toolbar.Realize()
        self.SetToolBar(toolbar)

        # Figure

        #### Sizer
        mainsizer = wx.GridBagSizer(3, 2)
        mainsizer.AddGrowableCol(1)
        mainsizer.AddGrowableRow(3)

        mainsizer.Add(self._spectrumViewerPanel, pos=(2,0))

        self.SetSizer(mainsizer)
        self.Fit()

        #### Bind
        self.Bind(wx.EVT_MENU, self.on_menu)
        self.Bind(wx.EVT_TOOL, self.on_toolbar)

    def GetRoot(self):
        logging.debug("MainFrame GetRoot called")
        return self

    def on_menu(self, event):
        """
        Handle menu click
        """
        logging.debug("MainFrame on_menu called")

        event_ID = event.GetId()

        if event_ID == wx.ID_OPEN:
            self._on_file_open_spectrum()
        elif event_ID == wx.ID_SAVE:
            self._on_file_save_spectrum()
        elif event_ID == wx.ID_SAVEAS:
            self._on_file_save_as_spectrum()
        elif event_ID == ID_SAVE_ALL:
            self._on_file_save_all_spectrum()
        elif event_ID == wx.ID_CLOSE:
            self._on_file_close_spectrum()
        elif event_ID == wx.ID_CLOSE_ALL:
            self._on_file_close_all_spectrum()
        elif event_ID == wx.ID_EXIT:
            self._on_file_exit()
        else:
            event.Skip()

    def on_toolbar(self, event):
        """
        Handle menu click
        """
        logging.debug("MainFrame on_toolbar called")

        self.on_menu(event)

    def _on_file_open_spectrum(self):
        logging.debug("MainFrame _on_file_open_spectrum called")

        style = wx.FD_OPEN | wx.FD_MULTIPLE
        wildcards = "Oxford instrument files (*.txt)|*.txt|EMSA files (*.emsa)|*.emsa|All files(*.*)|*.*"
        dialog = wx.FileDialog(self, "Open Spectrum", style=style, wildcard=wildcards)

        if dialog.ShowModal() == wx.ID_OK:
            filepaths = dialog.GetPaths()
            for filepath in filepaths:
                logging.debug("Filename: %s", filepath)

                with open(filepath, 'rb') as f:
                    self._spectra[filepath] = emsa.read(f)
                    self._currentSpectrumKey = filepath

        self.on_update()

    def _on_file_save_spectrum(self):
        logging.debug("MainFrame _on_file_save_spectrum called")
        logging.warning("Not implemented")

    def _on_file_save_as_spectrum(self):
        logging.debug("MainFrame _on_file_save_as_spectrum called")
        logging.warning("Not implemented")

    def _on_file_save_all_spectrum(self):
        logging.debug("MainFrame _on_file_save_all_spectrum called")
        logging.warning("Not implemented")

    def _on_file_close_spectrum(self):
        logging.debug("MainFrame _on_file_close_spectrum called")
        logging.warning("Not implemented")

    def _on_file_close_all_spectrum(self):
        logging.debug("MainFrame _on_file_close_all_spectrum called")
        logging.warning("Not implemented")

    def _on_file_exit(self):
        logging.debug("MainFrame _on_file_exit called")
        logging.warning("Not implemented")

    def on_close_series(self, event):
        logging.debug("MainFrame on_close_series called")

        index = event.GetSelection()
        self._viewer.series.pop(index)

    def on_update(self, event=None):
        logging.debug("MainFrame on_update called")

        spectrum = self._spectra[self._currentSpectrumKey]

        self._spectrumViewerPanel._viewer.xData = spectrum.xdata
        self._spectrumViewerPanel._viewer.yData = spectrum.ydata

        # Viewer
        self._spectrumViewerPanel._viewer.update()
        try:
            self._spectrumViewerPanel._viewer.update()
        except Exception as ex:
            logging.error(ex)
            return False

        return True

    def on_key_down(self, event):
        logging.debug("MainFrame on_key_down called")

        self.on_update()

    def on_save(self, event):
        logging.debug("MainFrame on_save called")

        # update to store all current parameters
        if not self.on_update():
            return

        # dialog
        wildcards = [("Viewer data file (*.dat)", "dat")]
        dialog = wx.FileDialog(None, wildcards, "Save", os.curdir, "", wx.FD_SAVE)

        if dialog.ShowModal() != wx.ID_OK:
            dialog.Destroy()
            return

        if not dialog.Validate():
            dialog.Destroy()
            self.on_save(event)
            return

        # save
        with open(dialog.GetPath(), 'w') as f:
            self._viewer.save(f)

        dialog.Destroy()
        os.chdir(os.path.dirname(dialog.GetPath()))

    def on_load(self, event):
        logging.debug("MainFrame on_load called")

        # dialog
        wildcards = [("Viewer data file (*.dat)", "dat")]
        dialog = wx.FileDialog(None, wildcards, "Open", os.curdir, "", wx.FD_OPEN)

        if dialog.ShowModal() != wx.ID_OK:
            dialog.Destroy()
            return

        if not dialog.Validate():
            dialog.Destroy()
            self.on_save(event)
            return

        # load
        with open(dialog.GetPath(), 'r') as f:
            self._viewer.load(f)

        # refresh GUI
        self._cb_xparams.SetSelectedObject(self._viewer.xParam)
        self._cb_yparams.SetSelectedObject(self._viewer.yParam)
        self._cb_ygrouping.SetSelectedObject(self._viewer.yGrouping)
        self._txt_condition.SetValue(str(self._viewer.condition))

        self._nb_series.DeleteAllPages()

        self.on_update()

        dialog.Destroy()
        os.chdir(os.path.dirname(dialog.GetPath()))

def run():
    logging.getLogger().setLevel(logging.DEBUG)
    app = wx.PySimpleApp()

    # Show main frame
    mainframe = MainFrame(None)
    mainframe.SetSizeWH(1200, 800)
    mainframe.Show()

    app.MainLoop()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
