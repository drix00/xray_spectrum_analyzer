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
try:
    import tkinter as Tk
except ImportError:
    import Tkinter as Tk

import logging
import os.path

# Third party modules.
from PIL import Image
from PIL import ImageTk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# Local modules.

# Globals and constants variables.

# TODO: Use option database for the appearance of the application.
# TODO: Check the name of widgets class.
# TODO: Check the name of widgets instance.

class MainWindow(Tk.Frame):
    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)

        # TODO: Cleanup set window dimension.
        #Set window dimension (minsize)
        if self.master != None:
            maxsize = self.master.maxsize()
            logging.debug("Master max size: %ix%i" % self.master.maxsize())
            logging.debug("Master min size: %ix%i" % self.master.minsize())
        else:
            maxsize = self.maxsize()

        self._minsize = (int(maxsize[0]/4), int(maxsize[1]/4))

        self.winfo_toplevel().minsize(self._minsize[0], self._minsize[1])

        self.grid_propagate(0)
        self["height"] = self._minsize[1]
        self["width"] = self._minsize[0]

        logging.debug("Max size: %ix%i" % maxsize)
        logging.debug("Min size: %ix%i" % self._minsize)

        #self.grid(sticky=Tk.N+Tk.E+Tk.S+Tk.W)
        self.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)

        self._createWidgets()

        # TODO: Still need these update and iconify/deiconify methods.
        self.update_idletasks()
        self.winfo_toplevel().update_idletasks()
        self.winfo_toplevel().update()

        self.winfo_toplevel().iconify()
        self.winfo_toplevel().deiconify()

        self._logInfo()

    def _createWidgets(self):
        self._createMenuBar()

        self._createToolBar()

        self._createMainArea()

        self._createStatusBar()

    def _createToolBar(self):
        # TODO: Move in a separated class.
        # DONE: Find a way to use image for button. Need to save ImageTk.
        self._toolBar = Tk.Frame(self, bd=1, relief=Tk.GROOVE)
        self._toolBar.pack(side=Tk.TOP, anchor=Tk.NW, fill=Tk.X, expand=Tk.NO)

        # TODO: Use configuration or auto-discovery to have the correct image path.
        baseImagePath = "/home/hdemers/works/prgrms/pythondev/SpectrumAnalyzer/images"

        try:
            imagePath = os.path.join(baseImagePath, "document-open.png")

            im = Image.open(imagePath)

            if im.mode != "RGB":
                im = im.convert("RGB")

            self._imTkOpenFile = ImageTk.PhotoImage(im)

            Tk.Button(self._toolBar, text='Open', image=self._imTkOpenFile, bd=1, relief=Tk.FLAT, command=self._openFile).pack(side=Tk.LEFT, anchor=Tk.NW, expand=Tk.NO)

        except:
            Tk.Button(self._toolBar, text='Open', bd=1, relief=Tk.FLAT, command=self._openFile).pack(side=Tk.LEFT, anchor=Tk.NW, expand=Tk.NO)

        try:
            imagePath = os.path.join(baseImagePath, "system-log-out.png")

            im = Image.open(imagePath)

            if im.mode != "RGB":
                    im = im.convert("RGB")

            self._imTkExit = ImageTk.PhotoImage(im)

            Tk.Button(self._toolBar, text='Exit', image=self._imTkExit, bd=1, relief=Tk.FLAT, command=self._exit).pack(side=Tk.LEFT, anchor=Tk.NW, expand=Tk.NO)

        except:
            Tk.Button(self._toolBar, text='Exit', bd=1, relief=Tk.FLAT, command=self._exit).pack(side=Tk.LEFT, anchor=Tk.NW, expand=Tk.NO)

        try:
            imagePath = os.path.join(baseImagePath, "help-browser.png")

            im = Image.open(imagePath)

            if im.mode != "RGB":
                im = im.convert("RGB")

            self._imTkHelp = ImageTk.PhotoImage(im)

            Tk.Button(self._toolBar, text='Help', image=self._imTkHelp, bd=1, relief=Tk.FLAT, command=self._help).pack(side=Tk.RIGHT, anchor=Tk.NW, expand=Tk.NO)

        except:
            Tk.Button(self._toolBar, text='Help', bd=1, relief=Tk.FLAT, command=self._help).pack(side=Tk.RIGHT, anchor=Tk.NE, expand=Tk.NO)

    def _createMenuBar(self):
        # TODO: Move in a separated class.
        self._menuBar = Tk.Frame(self, bd=2, relief=Tk.RAISED)
        self._menuBar.pack(side=Tk.TOP, anchor=Tk.NW, fill=Tk.X, expand=Tk.NO)

        # File menu.
        menuButton = Tk.Menubutton(self._menuBar, text="File", relief=Tk.FLAT)

        menuButton.menu = Tk.Menu(menuButton, tearoff=Tk.FALSE)
        menuButton['menu'] = menuButton.menu

        menuButton.menu.add_command(label='Open', command=self._openFile)
        menuButton.menu.add_separator()
        menuButton.menu.add_command(label='Exit', command=self._exit)

        menuButton.pack(side=Tk.LEFT, anchor=Tk.NW)

        # Help menu.
        menuButton = Tk.Menubutton(self._menuBar, text="Help", relief=Tk.FLAT)

        menuButton.menu = Tk.Menu(menuButton, tearoff=Tk.FALSE)
        menuButton['menu'] = menuButton.menu

        menuButton.menu.add_command(label='Help', command=self._help)
        menuButton.menu.add_separator()
        menuButton.menu.add_command(label='About', command=self._about)
        menuButton.pack(side=Tk.RIGHT, anchor=Tk.NE)

    def _createMainArea(self):
        # TODO: Move in a separated class.
        self._mainArea = Tk.Frame(self)
        self._mainArea.pack(side=Tk.TOP, anchor=Tk.NW, fill=Tk.BOTH, expand=Tk.YES)

        f = Figure(figsize=(2,1), dpi=100)

        # a tk.DrawingArea.
        canvas = FigureCanvasTkAgg(f, master=self._mainArea)
        canvas.show()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)

        toolbar = NavigationToolbar2TkAgg(canvas, self._mainArea)
        toolbar.update()
        canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)

    def _createStatusBar(self):
        # TODO: Move in a separated class.
        widthCharacters = 80

        self.statusBar = Tk.Label(self, justify=Tk.LEFT, anchor=Tk.W
                                                                                                                , relief=Tk.SUNKEN, bd=1, padx=0, pady=0
                                                                                                                , width=widthCharacters)
        self.text = ""
        self.statusBar.pack(side=Tk.BOTTOM, fill=Tk.X)

    def _openFile(self):
        logging.debug("Open file command")

    def _exit(self):
        logging.debug("Exit command")

        self.quit()

    def _help(self):
        logging.debug("Help command")

    def _about(self):
        logging.debug("About command")

    def quit(self, event=None):
        # Call parent's quit, for use with binding to 'q' and quit button.
        self.master.quit()

    def _logInfo(self):
        logging.debug("Class name info: %s" % self.winfo_class())
        logging.debug("Name info: %s" % self.winfo_name())
        logging.debug("Id info: %s" % self.winfo_id())
        logging.debug("Parent info: %s" % self.winfo_parent())
        logging.debug("Geometry info: %s" % self.winfo_geometry())
        logging.debug("Height info: %i" % self.winfo_height())
        logging.debug("Width info: %i" % self.winfo_width())
        logging.debug("Requested height info: %i" % self.winfo_reqheight())
        logging.debug("Requested width info: %i" % self.winfo_reqwidth())
        logging.debug("Screen height info (pixel): %i" % self.winfo_screenheight())
        logging.debug("Screen width info (pixel) : %i" % self.winfo_screenwidth())
        logging.debug("Screen height info (mm): %.1f" % self.winfo_screenmmheight())
        logging.debug("Screen width info (mm) : %.1f" % self.winfo_screenmmwidth())
        logging.debug("Screen color info: %s" % self.winfo_screenvisual())

        for index, children in enumerate(self.winfo_children()):
            args = (index, children.winfo_class(), children.winfo_name(), children.winfo_id())
            logging.debug("Children info %3i -> class: %s, name: %s, id: %s" % args)

def run(options, data, engine):
    mainWindow = MainWindow()

    mainWindow.master.title("Spectrum Analyzer")

    logging.info("Start main window main loop.")
    mainWindow.mainloop()

def main():
    run(None, None, None)

if __name__ == '__main__': #pragma: no cover
    main()
