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
from logging.handlers import RotatingFileHandler
import os

# Third party modules.
from PySide import QtCore
from PySide import QtGui
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Local modules.
import pyHendrixDemersTools.Files as Files
import pySpectrumAnalyzer.ui.console.SpectrumAnalyzer as SpectrumAnalyzer

# Project modules

# Globals and constants variables.

APPLICATION_NAME = "pySpectrumAnalyzer"
ORGANIZATION_NAME = "McGill University"
LOG_FILENAME = APPLICATION_NAME + '.log'

MODULE_LOGGER = logging.getLogger(APPLICATION_NAME)

class MainWindow(QtGui.QMainWindow):
    NumGridRows = 3

    def __init__(self):
        self.logger = logging.getLogger(APPLICATION_NAME + '.MainWindow')
        self.logger.info("MainWindow.__init__")

        super(MainWindow, self).__init__()

        QtGui.QIcon.setThemeSearchPaths(QtGui.QIcon.themeSearchPaths() + ["D:\work\codings\hendrix_demersBitbucket\pyspectrumanalyzer\resource\oxygen-icons-png-master"])
        QtGui.QIcon.setThemeName('oxygen')
        print(QtGui.QIcon.fromTheme('document-save').isNull())
        self.create_gui()

        currentPath = Files.getCurrentModulePath(__file__)
        configurationFilepath = os.path.join(currentPath, "../../../SpectrumAnalyzer.cfg")

        self.spectrumAnalyzer = SpectrumAnalyzer.SpectrumAnalyzer(configurationFilepath=configurationFilepath, keepGraphic=False)

# TODO: Add Menubar
# TODO: Add statusbar
# TODO: Save project (autosave)
# TODO: Add toolbars
# TODO: Add spectrum list
# TODO: Add spectrum display
# TODO: Add ROI list
# TODO: Add ROI display
# TODO: Elements list
# TODO: Element+line display
# TODO: Add main window
# TODO: Add layout management
# TODO: Add log file
# TODO: Fit dialog recipe
# TODO: Add drag and drop

    def create_gui(self):
        self.logger.info("MainWindow.create_gui")

        self._create_main_window()
        self._create_actions()
        self._create_menus()
        self._create_toolbars()
        self._create_tooltip()
        self._create_spectra_display()
        self._create_data_display()
        self._create_operations_display()
        self._create_layout()
        self._create_statusbar()

        self._read_settings()

        self.show()

    def _create_main_window(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Spectrum Analyzer')
        #self.setWindowIcon(QtGui.QIcon('../../../images/cog.svg'))
        self.setWindowIcon(self.style().standardIcon(QtGui.QStyle.SP_DesktopIcon))
        self._center_main_window()

    def _center_main_window(self):
        self.logger.info("MainWindow._center_main_window")

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_menus(self):
        self.logger.info("MainWindow._create_menus")

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def _create_layout(self):
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        mainLayout.addWidget(self.plotGroupBox)
        mainLayout.addWidget(self.operationsGroupBox)

        self.mainGroupBox = QtGui.QGroupBox("Main layout")
        self.mainGroupBox.setLayout(mainLayout)
        self.setCentralWidget(self.mainGroupBox)

    def _create_spectra_display(self):
        self.plotGroupBox = QtGui.QGroupBox("Plot layout")

        self.figure1 = Figure(facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setParent(self.plotGroupBox)
        self.canvas1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas1.setFocus()
        self.canvas1.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.canvas1.updateGeometry()

        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.plotGroupBox)
        self.canvas1.mpl_connect('key_press_event', self.on_key_press)

        self.figure2 = Figure(facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setParent(self.plotGroupBox)
        self.mpl_toolbar2 = NavigationToolbar(self.canvas1, self.plotGroupBox)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas1)
        layout.addWidget(self.mpl_toolbar1)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.mpl_toolbar2)
        self.plotGroupBox.setLayout(layout)

    def _create_data_display(self):
        self.dataGroupBox = QtGui.QGroupBox("Data layout")
        data_layout = QtGui.QVBoxLayout()

        group_box = QtGui.QGroupBox("Spectra")
        self.spectra_list_view = QtGui.QListWidget(self)
        self.spectra_list_view.setMinimumWidth(200)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.spectra_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        group_box = QtGui.QGroupBox("ROI")
        roi_list_view = QtGui.QListWidget(self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(roi_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        group_box = QtGui.QGroupBox("Elements")
        element_list_view = QtGui.QListWidget(self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(element_list_view)
        group_box.setLayout(layout)
        data_layout.addWidget(group_box)

        self.dataGroupBox.setLayout(data_layout)

    def _create_operations_display(self):
        self.operationsGroupBox = QtGui.QGroupBox("Operations layout")
        results_layout = QtGui.QVBoxLayout()

        group_box = QtGui.QGroupBox("Operation")
        results_layout.addWidget(group_box)
        group_box = QtGui.QGroupBox("Results")
        results_layout.addWidget(group_box)

        self.operationsGroupBox.setLayout(results_layout)

    def _create_tooltip(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

    def _create_actions(self):
        self.logger.info("MainWindow._create_actions")

        self.newAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_FileIcon), "&New",
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon),
                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton),
                "&Save", self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton), "Save &As...", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.exitAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton),
                                     "E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.textEdit = QtGui.QTextEdit()

        self.aboutAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_MessageBoxInformation), "&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_TitleBarMenuButton), "About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def _create_toolbars(self):
        self.logger.info("MainWindow._create_toolbars")

        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

    def _create_statusbar(self):
        self.logger.info("MainWindow._create_statusbar")

        self.statusBar().showMessage("Ready")

    def _read_settings(self):
        self.logger.info("MainWindow._read_settings")

        settings = QtCore.QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def _write_settings(self):
        self.logger.info("MainWindow._write_settings")

        settings = QtCore.QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        self.logger.info("MainWindow.maybeSave")

        if self.textEdit.document().isModified():
            ret = QtGui.QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        self.logger.info("MainWindow.closeEvent")

        if self.maybeSave():
            self._write_settings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        self.logger.info("MainWindow.newFile")

        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        self.logger.info("MainWindow.open")

        if self.maybeSave():
            filepath, _filtr = QtGui.QFileDialog.getOpenFileName(self)
            if filepath:
                self.spectrumAnalyzer.readSpectrum(filepath)
                filename = os.path.basename(filepath)
                self.spectra_list_view.addItem(filename)
                self.spectrumAnalyzer.plotSpectrum(self.figure1)
                self.canvas1.draw()

    def save(self):
        self.logger.info("MainWindow.save")

        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        self.logger.info("MainWindow.saveAs")

        fileName, _filtr = QtGui.QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        self.logger.info("MainWindow.about")

        QtGui.QMessageBox.about(self, "About pySpectrumAnalyzer",
                "The <b>pySpectrumAnalyzer</b> extract peak intensity from EDS spectrum.")

    def documentWasModified(self):
        self.logger.info("MainWindow.documentWasModified")

        self.setWindowModified(self.textEdit.document().isModified())

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas1, self.mpl_toolbar1)

# TODO: Add background models.
# TODO: Add FFT filters
# TODO: Add find hidden peaks
# TODO: Add ROI manager
# TODO: Add Detector efficiency manager
# TODO: Add sum peak corrections
# TODO: Add peak finder
# TODO: Add detector artifacts
# TODO: Add results table
# TODO: Element identifications
# TODO: Background estimation
# TODO: Results display
# TODO: Specimen description: coating
# TODO: Predefined elements
# TODO: Normalized spectra: point and region
# TODO: Noise peak
# TODO: Confirm elements
# TODO: Detector parameters
# TODO: Energy-channel calibration
# TODO: Reference spectra
# TODO: instrument parameters


def createApplication():
    application = QtGui.QApplication(sys.argv)
    application.setApplicationName(APPLICATION_NAME)
    application.setOrganizationName(ORGANIZATION_NAME)

    return application


def startLogging():
    dataLocation = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation)
    if not os.path.isdir(dataLocation):
        os.makedirs(dataLocation)

    logFilepath = os.path.join(dataLocation, LOG_FILENAME)
    fh = RotatingFileHandler(logFilepath, maxBytes=1024*30, backupCount=10)
    MODULE_LOGGER.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    fh.setFormatter(formatter)
    MODULE_LOGGER.addHandler(fh)
    MODULE_LOGGER.info("startLogging")

    MODULE_LOGGER.debug("Data location: %s", dataLocation)
    MODULE_LOGGER.debug("Applications location: %s", QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.ApplicationsLocation))
    MODULE_LOGGER.debug("Home location: %s", QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation))
    MODULE_LOGGER.debug("Temp location: %s", QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.TempLocation))
    MODULE_LOGGER.debug("Cache location: %s", QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.CacheLocation))


def run():
    # Note application and mainWin have to be declared in the same method.
    application = createApplication()
    startLogging()

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(application.exec_())


if __name__ == '__main__': #pragma: no cover
    run()
