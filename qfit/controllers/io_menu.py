
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
)

from qfit.models.registry import Registry

from qfit.widgets.menu import MenuWidget

from qfit.core.helpers import StopExecution

from qfit.io_utils.measurement_file_readers import readMeasurementFile

import sys
import os

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import MeasurementDataType


class IOMenuCtrl:
    """
    This controller handles the menu bar and related IO operations, including:
    - new project
    - open file
    - save file
    - save file as
    - close app
    
    # TODO:
    - export hs?
    - export extracted data?

    """
    def __init__(
        self, 
        menu: MenuWidget, 
        registry: Registry,
        mainWindow: "MainWindow",
    ):
        self.menu = menu
        self.registry = registry
        self.mainWindow = mainWindow

        self.setConnects()
        self.mainWindow.register()

    def setConnects(self):
        self.mainWindow.ui.toggleMenuButton.clicked.connect(self.menu.toggle)

        self.menu.ui.menuQuitButton.clicked.connect(self.mainWindow.close)
        self.menu.ui.menuOpenButton.clicked.connect(self.openFile)
        self.menu.ui.menuNewButton.clicked.connect(self.newProject)
        self.menu.ui.menuSaveButton.clicked.connect(self.saveFile)
        self.menu.ui.menuSaveAsButton.clicked.connect(self.saveFileAs)

    @staticmethod
    def measurementDataFromFile(
        fileName: str,
    ):
        """
        A convenient way to call 
        qfit.io_utils.measurement_file_readers.readMeasurementFile
        """
        return readMeasurementFile(fileName)
    
    @staticmethod
    def registryFromFile(
        fileName: str,
    ):
        """
        A convenient way to call qfit.models.registry.Registry.fromFile
        """
        return Registry.fromFile(fileName)
        

    def _importMeasurementData(
        self, 
        home = None,
    ) -> "MeasurementDataType":
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
            fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open", home, fileCategories)
            if not fileName:
                self.closeApp()
                raise StopExecution

            measurementData = self.measurementDataFromFile(fileName)

            if measurementData is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error opening file.")
                msg.setInformativeText(
                    "The selected file format is supported, but heuristic inspection "
                    "failed to identify suitable data inside the file."
                )
                msg.setWindowTitle("Error")
                _ = msg.exec_()
            else:
                break

        return measurementData

    def _importProject(
        self,
        home = None,
    ) -> Registry:
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Qfit project (*.qfit)"
            fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open", home, fileCategories)
            if not fileName:
                self.closeApp()
                raise StopExecution

            registry = self.registryFromFile(fileName)

            if registry is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error opening file.")
                msg.setInformativeText(
                    "File is not found."
                )
                msg.setWindowTitle("Error")
                _ = msg.exec_()
            else:
                break

        return registry
    
    def _saveProject(
        self,
        home = None,
        save_as: bool = False,
    ):
        # choose a home directory
        if self.mainWindow.projectFile is not None:
            home = os.path.dirname(self.mainWindow.projectFile)
        else:
            if home is None:
                home = os.path.expanduser("~")

        # find a suitable filename
        if save_as or self.mainWindow.projectFile is None:
            while True:
                fileCategories = "Qfit project (*.qfit)"
                fileName, _ = QFileDialog.getSaveFileName(self.mainWindow, "Save as", home, fileCategories)
                
                # check whether the filename is valid 
                if fileName is None:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Invalid filename.")
                    msg.setInformativeText(
                        "Please enter a valid filename."
                    )
                    msg.setWindowTitle("Warning")
                    _ = msg.exec_()
                    continue

                # check whether the filename ends with .qfit
                if not fileName.endswith(".qfit"):
                    fileName = fileName + ".qfit"

                # # check whether the file exists, actually this is not
                # # needed and will be handled by QFileDialog.getSaveFileName
                # if os.path.exists(fileName):
                #     msg = QMessageBox()
                #     msg.setIcon(QMessageBox.Warning)
                #     msg.setText("File already exists.")
                #     msg.setInformativeText(
                #         "File already exists. Do you want to overwrite it?"
                #     )
                #     msg.setWindowTitle("Warning")
                #     msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                #     msg.setDefaultButton(QMessageBox.No)
                #     reply = msg.exec_()
                #     if reply == QMessageBox.Yes:
                #         break
                #     elif reply == QMessageBox.No:
                #         continue
                #     else:   # reply == QMessageBox.Cancel
                #         return 
                else:
                    break
        else:
            fileName = self.mainWindow.projectFile

        # save the project
        self.registry.exportPkl(fileName) 
        self.mainWindow.projectFile = fileName

    def newProjectWithData(self, measurementData: "MeasurementDataType"):
        """
        New project with measurement data (keep hilbertspace the same)
        To load a measurementData from file, use ioMenuCtrl.measurementDataFromFile
        """
        self.mainWindow.initializeDynamicalElements(
            hilbertspace = self.mainWindow.hilbertspace,
            measurementData = measurementData,
        )
    
    def newProjectWithRegistry(self, registry: Registry):
        """
        New project with a exsisted registry object.
        To load a registry from file, use ioMenuCtrl.registryFromFile
        """
        self.mainWindow.initializeDynamicalElements(
            hilbertspace = registry["hilbertspace"],
            measurementData = registry["measurementData"],
        )

    @Slot()
    def newProject(self, from_menu: bool = True):
        measurementData = self._importMeasurementData()

        self.newProjectWithData(measurementData)

        if not from_menu:
            self.menu.toggle()
        
    @Slot()
    def openFile(self, from_menu: bool = True):
        registry = self._importProject()

        self.newProjectWithRegistry(registry)

        if not from_menu:
            self.menu.toggle()

    def _quit(self):
        if self.mainWindow.openFromIPython:
            self.closeAppIPython()
        else:
            sys.exit()

    def closeApp(self) -> bool:
        """End the application"""
        if self.mainWindow.allDatasets.isEmpty():
            # if run through ipython, no need to perform sys.exit, just close and delete
            # the window
            self._quit()
            return True
            
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("qfit")
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setInformativeText("Do you want to save changes?")
            msgBox.setText("This document has been modified.")
            msgBox.setStandardButtons(
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            msgBox.setDefaultButton(QMessageBox.Save)

            reply = msgBox.exec_()

            if reply == QMessageBox.Save:
                self.saveAndCloseApp()
                return True
            elif reply == QMessageBox.Discard:
                self._quit()
                return True
            else:   # reply == QMessageBox.Cancel
                self.menu.toggle()
                return False

    def closeAppIPython(self):
        """
        Close the app when running in ipython
        """
        self.mainWindow.close()
        self.mainWindow.deleteLater()
        self.mainWindow.destroy()
        # raise StopExecution

    @Slot()
    def saveFile(self):
        """Save the extracted data and calibration information to file."""
        self._saveProject(save_as = False)

        self.menu.toggle()

    @Slot()
    def saveFileAs(self):
        """Save the extracted data and calibration information to file."""
        self._saveProject(save_as = True)

        self.menu.toggle()

    @Slot()
    def saveAndCloseApp(self):
        """Save the extracted data and calibration information to file, then exit the
        application."""
        success = self.saveFile()
        if not success:
            return
        self._quit()
