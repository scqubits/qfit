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

from typing import TYPE_CHECKING, Union, Dict, Any

from qfit.models.measurement_data import (
    ImageMeasurementData,
    NumericalMeasurementData,
)

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import (
        MeasurementDataType,
    )


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
    def registryDictFromFile(
        fileName: str,
    ) -> Union[Dict[str, Any], None]:
        """
        A convenient way to call qfit.models.registry.Registry.fromFile
        """
        return Registry.fromFile(fileName)
        
    def _importMeasurementData(
        self,
        home=None,
    ) -> "MeasurementDataType":
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
            fileName, _ = QFileDialog.getOpenFileName(
                self.mainWindow, "Open", home, fileCategories
            )
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
        home=None,
    ) -> Dict[str, Any]:
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Qfit project (*.qfit)"
            fileName, _ = QFileDialog.getOpenFileName(
                self.mainWindow, "Open", home, fileCategories
            )
            if not fileName:
                self.closeApp()
                raise StopExecution

            registryDict = self.registryDictFromFile(fileName)

            if registryDict is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error opening file.")
                msg.setInformativeText("File is not found.")
                msg.setWindowTitle("Error")
                _ = msg.exec_()
            else:
                break

        return registryDict

    def _saveProject(
        self,
        home=None,
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
                fileName, _ = QFileDialog.getSaveFileName(
                    self.mainWindow, "Save as", home, fileCategories
                )

                if fileName is None:
                    print("Save cancelled.")
                    return

                # check whether the filename ends with .qfit
                if not fileName.endswith(".qfit"):
                    fileName = fileName + ".qfit"

                else:
                    break
        else:
            fileName = self.mainWindow.projectFile

        # update the project file name, must be done before saving the project,
        # as when loaded, the projectFile should be the same as the file name
        self.mainWindow.projectFile = fileName

        # save the project
        self.registry.exportPkl(fileName)

    def newProjectWithData(self, measurementData: "MeasurementDataType"):
        """
        New project with measurement data (keep hilbertspace the same)
        To load a measurementData from file, use ioMenuCtrl.measurementDataFromFile
        """
        self.mainWindow.initializeDynamicalElements(
            hilbertspace=self.mainWindow.hilbertspace,
            measurementData=measurementData,
        )
    
    def newProjectWithRegistryDict(self, registryDict: Dict[str, Any]):
        """
        New project with a exsisted registry object. Will do the following:
        - partially update the registry: hilbertspace, measurementData
        - update the dynamical elements in the main window
        - update the rest of the registry (by calling setters)

        To load a registry from file, use ioMenuCtrl.registryFromFile
        """
        # load the hilbertspace and measurementData
        hilbertspace = registryDict["HilbertSpace"]
        dateType = globals()[registryDict["measurementData.type"]]
        measurementData = dateType(*registryDict["measurementData.args"])

        # update the dynamical elements in the main window
        self.mainWindow.initializeDynamicalElements(
            hilbertspace=hilbertspace,
            measurementData=measurementData,
        )

        # update the rest of the registry
        self.registry.setByDict(registryDict)

    @Slot()
    def newProject(self, from_menu: bool = True):
        measurementData = self._importMeasurementData()

        self.newProjectWithData(measurementData)

        if not from_menu:
            self.menu.toggle()

    @Slot()
    def openFile(self, from_menu: bool = True):
        registryDict = self._importProject()

        self.newProjectWithRegistryDict(registryDict)
        # hilbertspace

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
            else:  # reply == QMessageBox.Cancel
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
        self._saveProject(save_as=False)

        self.menu.toggle()

    @Slot()
    def saveFileAs(self):
        """Save the extracted data and calibration information to file."""
        self._saveProject(save_as=True)

        self.menu.toggle()

    @Slot()
    def saveAndCloseApp(self):
        """Save the extracted data and calibration information to file, then exit the
        application."""
        success = self.saveFile()
        if not success:
            return
        self._quit()
