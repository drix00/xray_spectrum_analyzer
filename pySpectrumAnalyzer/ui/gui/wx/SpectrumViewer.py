#!/usr/bin/env python
"""
.. py:currentmodule:: gui.SpectrumViewer
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Spectrum viewer
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
import pickle

# Third party modules.
import numpy as np

from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg

import wx
from wx.lib.embeddedimage import PyEmbeddedImage

from wxtools.messagedialog import show_error_dialog

# Local modules.

# Project modules

# Globals and constants variables.
SELECT_IMAGE = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlw"
    "SFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoA"
    "AAE5SURBVEiJ7ZYxSkNREEXPzQsWFtaWwi/sJCCWugRJpb0LMK0LsIidbsFGCFhJsLAxtYUh"
    "uAcVLaw0Isy1+ZGfRJGYH0HwVvOmuId5w5t5ss0sVZmpO1AFkFQDaiV7d213q/mhDmwBvZLM"
    "V4AW8AEAOKtUKq8R0bT9PI27pOYgLvbAwLKknqSNaQBFDTU5ItpAJukypXQkab5UAHAOBCDb"
    "u3k166UBbD8AV4VUJqmTUjr8aTVj78B2eyQl2w1JHUmLUwOAIYCkE9tZRKzZvisDcA3cAm+2"
    "92zXgYVJjQeqjiZsO6XUBvoRcZBSyoBTSau2nyYFfDqLIqIVEft53AD6ko4lqRSA7Qvb93n8"
    "Yntb0iMwNylg7Iq+AN4AO5Oawy+M63/Atyo2eVPSUkm+g4WDbM90ZerP/yreASWugLcL8HvE"
    "AAAAAElFTkSuQmCC")

class NavigationToolbar(NavigationToolbar2WxAgg):
    def __init__(self, canvas, viewer):
        NavigationToolbar2WxAgg.__init__(self, canvas)

        # Variables
        self._viewer = viewer

    def _init_toolbar(self):
        NavigationToolbar2WxAgg._init_toolbar(self)

        self._NTB_SELECT = wx.NewId()

        self.AddSeparator()
        self.AddCheckTool(self._NTB_SELECT, SELECT_IMAGE.getBitmap(),
                          shortHelp='Select', longHelp='Select ids over an area')

        self.Bind(wx.EVT_TOOL, self.select, id=self._NTB_SELECT)

        self.Realize()

    def mouse_move(self, event):
        NavigationToolbar2WxAgg.mouse_move(self, event)

        if self._active == 'SELECT':
            if self._xypress:
                x, y = event.x, event.y
                lastx, lasty, _lastxdata, _lastydata = self._xypress[0]
                self.draw_rubberband(event, x, y, lastx, lasty)

    def zoom(self, *args):
        self.ToggleTool(self._NTB_SELECT, False)
        NavigationToolbar2WxAgg.zoom(self, *args)

    def pan(self, *args):
        self.ToggleTool(self._NTB_SELECT, False)
        NavigationToolbar2WxAgg.pan(self, *args)

    def select(self, event):
        self.ToggleTool(self._NTB2_PAN, False)
        self.ToggleTool(self._NTB2_ZOOM, False)

        if self._active == 'SELECT':
            self._active = None
        else:
            self._active = 'SELECT'

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''

        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if self._active:
            self._idPress = self.canvas.mpl_connect('button_press_event',
                                                    self.press_select)
            self._idRelease = self.canvas.mpl_connect('button_release_event',
                                                      self.release_select)
            self.mode = 'select'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)

    def press_select(self, event):
        x, y = event.x, event.y
        if x is None or y is None:
            return
        xdata, ydata = event.xdata, event.ydata

        self._xypress = []
        self._xypress.append((x, y, xdata, ydata))

        self.press(event)

    def release_select(self, event):
        if not self._xypress:
            return
        lastx, lasty, lastxdata, lastydata = self._xypress[0]

        x, y = event.x, event.y
        if x is None or y is None:
            return
        xdata, ydata = event.xdata, event.ydata

        # ignore singular clicks - 5 pixels is a threshold
        if abs(x - lastx) < 5 or abs(y - lasty) < 5:
            self._xypress = None
            self.release(event)
            self.draw()
            return

        # get values
        x0 = min(xdata, lastxdata)
        x1 = max(xdata, lastxdata)
        y0 = min(ydata, lastydata)
        y1 = max(ydata, lastydata)

        # keys
        if self._viewer.xParam is None or self._viewer.yParam is None:
            show_error_dialog(None, "No parameter selected for x and/or y")
            self._xypress = None
            self.release(event)
            self.draw()
            return
        xKey = self._viewer.xParam.key
        yKey = self._viewer.yParam.key

        # expression
        expr = str(self._viewer.condition)
        if expr.strip() != "":
            expr += " and "
        expr += "{%s} >= %f and {%s} <= %f" % (xKey, x0, xKey, x1)
        if expr.strip() != "":
            expr += " and "
        expr += "{%s} >= %f and {%s} <= %f" % (yKey, y0, yKey, y1)

        # evaluate expression
        series_ids_dict = {}

        for listener in self._viewer.listeners:
            listener.on_pick(series_ids_dict)

        # Reset everything
        self.draw()
        self._xypress = None
        self._button_pressed = None
        self.push_current()
        self.release(event)

        self.ToggleTool(self._NTB_SELECT, False)
        self._active = None
        self.canvas.mpl_disconnect(self._idPress)
        self.canvas.mpl_disconnect(self._idRelease)

class SpectrumViewer(object):
    def __init__(self, fig):

        # Configuration
        self.xData = []
        self.yData = []

        self.xParam = None
        self.yParam = None
        self.yGrouping = None
        self.series = []
        self._artists = {}

        self.fig = fig
        self.ax = self.fig.add_subplot("111")
        if self.fig.canvas:
            self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        self.listeners = []

    def on_pick(self, event):
        if event.artist not in self._artists.keys():
            return True

        if not len(event.ind):
            return True

        # click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        # data
        series, ids, xs, ys = self._artists[event.artist]
        xs = np.array(xs)
        ys = np.array(ys)

        distances = np.hypot(x - xs[event.ind], y - ys[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.selected.set_visible(True)
        self.selected.set_data(xs[dataind], ys[dataind])
        self.fig.canvas.draw()

        for listener in self.listeners:
            listener.on_pick({series: ids[dataind]})

    def update(self):
        self.ax.cla()
        self._artists.clear()

        self.ax.plot(self.xData, self.yData)

        self.fig.canvas.draw()

    def save(self, fileobj):
        odict = {'xParam': self.xParam,
                 'yParam': self.yParam,
                 'yGrouping': self.yGrouping,
                 'condition': self.condition,
                 'series': self.series}

        pickle.dump(odict, fileobj)

    def load(self, fileobj):
        idict = pickle.load(fileobj)

        self.xParam = idict['xParam']
        self.yParam = idict['yParam']
        self.yGrouping = idict['yGrouping']
        self.condition = idict['condition']
        self.series = idict['series']


if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
