#!/usr/bin/env python
"""
.. py:currentmodule:: ui.gui.pyside.mainWindow
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Spectrum Analyzer main window.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import sys
import logging

# Third party modules.
from PySide import QtCore
from PySide import QtGui

# Local modules.

# Project modules

# Globals and constants variables.

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)


        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('Close the application')
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 50)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Spectum Analyzer')
        self.setWindowIcon(QtGui.QIcon('../../../images/cog-8x.png'))
        self.center()

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def run():
    # Create a Qt application.
    app = QtGui.QApplication(sys.argv)

    # Create a Label and show it.
    mainWindow = MainWindow()

    # Enter Qt application main loop.
    app.exec_()
    sys.exit()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
