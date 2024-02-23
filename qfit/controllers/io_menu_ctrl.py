import sys
import os
import numpy as np
import copy

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
)

from scqubits.core.hilbert_space import HilbertSpace

from qfit.models.registry import Registry
from qfit.widgets.menu import MenuWidget
from qfit.utils.helpers import StopExecution
from qfit.io_utils.measurement_file_readers import readMeasurementFile

# This import is necessary for the registry (in method openProjectWithRegistryDict)
from qfit.models.measurement_data import (
    ImageMeasurementData,
    NumericalMeasurementData,
)

from typing import TYPE_CHECKING, Union, Dict, Any, Optional, List

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import (
        MeasurementDataType,
    )


class IOCtrl:
    """
    This controller handles the menu bar and related IO operations, including:
    - new project
    - open file
    - save file
    - save file as
    - close app

    It will run the mainWindow.register() when created.

    # TODO:
    - rename io_menu.py to a better name!!!


    Parameters
    ----------
    menu : MenuWidget
        The menu widget that provides the buttons, including:
        - toggleMenuButton
        - menuQuitButton
        - menuOpenButton
        - menuNewButton
        - menuSaveButton
        - menuSaveAsButton
    registry : Registry
        The registry object.
    mainWindow : MainWindow
        The main window object.
    """

    def __init__(
        self,
        ui_Menu: MenuWidget,
        registry: Registry,
        mainWindow: "MainWindow",  # it's not a good idea to use the entire
        # main window here, but this IO controller
        # really needs great power - initialize
        # the dynamical elements, save the project,
        # close the app, etc.
    ):
        self.menu = ui_Menu
        self.registry = registry
        self.mainWindow = mainWindow

        self.setConnects()

    def setConnects(self):
        """
        Connect the buttons to the corresponding functions, including
        - toggle
        - quit
        - open
        - new
        - save
        - save as
        """
        self.mainWindow.ui.toggleMenuButton.clicked.connect(self.menu.toggle)

        self.menu.ui.menuQuitButton.clicked.connect(self.mainWindow.close)
        self.menu.ui.menuOpenButton.clicked.connect(self.openFile)
        self.menu.ui.menuNewButton.clicked.connect(self.newProject)
        self.menu.ui.menuSaveButton.clicked.connect(self.saveFile)
        self.menu.ui.menuSaveAsButton.clicked.connect(self.saveFileAs)

    # load ####################################################################
    @staticmethod
    def _measurementDataFromFile(
        fileName: str,
    ) -> "MeasurementDataType":
        """
        Read the measurement data from the given file.

        Serves as a convenient way to call
        `qfit.io_utils.measurement_file_readers.readMeasurementFile`.
        """
        return readMeasurementFile(fileName)

    @staticmethod
    def _registryDictFromFile(
        fileName: str,
    ) -> Union[Dict[str, Any], None]:
        """
        Read the registryDict from the given file.

        Serves as a convenient way to call
        `qfit.models.registry.Registry.fromFile`.
        """
        return Registry.fromFile(fileName)

    def _measurementDataFromDialog(
        self,
        home=None,
        window_initialized=False,
    ) -> Union["MeasurementDataType", None]:
        """
        Open a dialog to select a file, then read the measurement data from the file.
        """
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
            fileName, _ = QFileDialog.getOpenFileName(
                self.mainWindow, "Open", home, fileCategories
            )
            if not fileName:
                if not window_initialized:
                    self.closeApp()
                    raise StopExecution
                else:
                    return None

            measurementData = self._measurementDataFromFile(fileName)

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

        # set the focus to the main window after opening a file
        self.mainWindow.activateWindow()

        return measurementData

    def _registryDictFromDialog(
        self,
        home=None,
        window_initialized=False,
    ) -> Union[Dict[str, Any], None]:
        """
        Open a dialog to select a file, then read the registryDict from the file.
        """
        if home is None:
            home = os.path.expanduser("~")

        while True:
            fileCategories = "Qfit project (*.qfit)"
            fileName, _ = QFileDialog.getOpenFileName(
                self.mainWindow, "Open", home, fileCategories
            )
            if not fileName:
                if not window_initialized:
                    self.closeApp()
                    raise StopExecution
                else:
                    return None

            registryDict = self._registryDictFromFile(fileName)

            if registryDict is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error opening file.")
                msg.setInformativeText("File is not found.")
                msg.setWindowTitle("Error")
                _ = msg.exec_()
            else:
                break

        # set the focus to the main window after opening a file
        self.mainWindow.activateWindow()

        return registryDict

    # save ####################################################################
    def _saveProject(
        self,
        home=None,
        save_as: bool = False,
    ):
        """
        Open a dialog to select a file, then save the project to the file.
        """
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
                if not fileName:
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

    # new #####################################################################
    def newProjectWithMeasurementData(
        self, 
        hilbertspace: HilbertSpace,
        measurementData: List["MeasurementDataType"]
    ):
        """
        New project with measurement data (keep hilbertspace the same)
        To load a measurementData from file, use ioMenuCtrl.measurementDataFromFile
        """
        self.mainWindow.initializeDynamicalElements(
            hilbertspace=hilbertspace,
            measurementData=measurementData,
        )

    # open ####################################################################
    def openProjectWithRegistryDict(self, registryDict: Dict[str, Any]):
        """
        New project with a exsisted registry object. Will do the following:
        - partially update the registry: hilbertspace, measurementData
        - update the dynamical elements in the main window
        - update the rest of the registry (by calling setters)

        To load a registry from file, use ioMenuCtrl.registryFromFile
        """
        # load the hilbertspace and measurementData
        hilbertspace = registryDict["HilbertSpace"]
        measurementData = registryDict["measDataSet.data"]

        # update the dynamical elements in the main window (i.e. load from the registry
        # the r entries)
        self.mainWindow.initializeDynamicalElements(
            hilbertspace=hilbertspace,
            measurementData=measurementData,
        )

        # update the rest of the registry (i.e. those entries with r+)
        self.registry.setByDict(registryDict)

        self.mainWindow.unsavedChanges = False

    # quit / close ############################################################
    def _quit(self):
        if self.mainWindow.openFromIPython:
            self.closeAppIPython()
        else:
            sys.exit()

    def closeApp(self) -> bool:
        """End the application"""
        # first, if the project is open from a file, check the registry dict of the old file
        # with that obtained from the current session, if something changed, ask the user
        # whether to save the changes
        if self.mainWindow.projectFile is not None:
            registryDict = copy.deepcopy(self.registry.exportDict())
            registryDictFromFile = copy.deepcopy(
                self._registryDictFromFile(self.mainWindow.projectFile)
            )
            assert registryDictFromFile is not None, "File not found"
            # remove HilbertSpace and file name from these dicts
            registryDict.pop("HilbertSpace")
            registryDictFromFile.pop("HilbertSpace")
            registryDict.pop("projectFile")
            registryDictFromFile.pop("projectFile")
            currentTagList = registryDict["allExtractedData"]["taglist"]
            fileTagList = registryDictFromFile["allExtractedData"]["taglist"]
            if len(currentTagList) != len(fileTagList):
                self.mainWindow.unsavedChanges = True
            else:
                for currentTag, fileTag in zip(currentTagList, fileTagList):
                    # compare each tag attribute-by-attribute
                    if currentTag.__dict__ != fileTag.__dict__:
                        self.mainWindow.unsavedChanges = True
                        break
            registryDict["allExtractedData"].pop("taglist")
            registryDictFromFile["allExtractedData"].pop("taglist")
            # use numpy.testing.assert_equal to check equality for the rest of the dict
            try:
                np.testing.assert_equal(
                    registryDict, registryDictFromFile, verbose=True
                )
            except AssertionError:
                self.mainWindow.unsavedChanges = True

            # for key, value in registryDictFromFile.items():
            #     if key in {"HilbertSpace", "measurementData.args"}:
            #         continue
            #     if key not in registryDict:
            #         self.mainWindow.unsavedChanges = True
            #         break
            #     if type(value) is np.ndarray:
            #         if (value != registryDict[key]).any():
            #             self.mainWindow.unsavedChanges = True
            #             break
            #     else:
            #         print(value)
            #         if value != registryDict[key]:
            #             self.mainWindow.unsavedChanges = True
            #             break
        else:
            self.mainWindow.unsavedChanges = True
            if self.mainWindow.allDatasets.isEmpty():
                self.mainWindow.unsavedChanges = False
        if self.mainWindow.unsavedChanges:
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

        else:
            self._quit()
            return True

    def closeAppIPython(self):
        """
        Close the app when running in ipython
        """
        self.mainWindow.close()
        self.mainWindow.deleteLater()
        self.mainWindow.destroy()
        # raise StopExecution

    # export ##################################################################
    def exportParameters(self) -> Dict[str, Any]:
        """
        Return the parameters as a dict.
        """
        return self.mainWindow.fitParamModel.getAttrDict("value")

    def exportHilbertSpace(self, deepcopy: bool = False) -> HilbertSpace:
        """
        Return the hilbert space object.
        """
        if deepcopy:
            return copy.deepcopy(self.mainWindow.quantumModel.hilbertspace)
        return self.mainWindow.quantumModel.hilbertspace

    # slots ###################################################################
    @Slot()
    def newProject(
        self, 
        __value=None, 
        from_menu: bool = True, 
        hilbertSpace: Optional[HilbertSpace] = None
    ):
        """
        Open a dialog to select a measurement file, then create a new project
        """
        if from_menu:
            self.menu.toggle()

        measurementData = self._measurementDataFromDialog(window_initialized=from_menu)
        if measurementData is None:
            return

        if hilbertSpace is None:
            hilbertSpace = self.mainWindow.quantumModel.hilbertspace

        self.newProjectWithMeasurementData(hilbertSpace, [measurementData])

    @Slot()
    def openFile(self, __value=None, from_menu: bool = True):
        """
        Open a dialog to select a project file, then open the project
        """
        if from_menu:
            self.menu.toggle()

        registryDict = self._registryDictFromDialog(window_initialized=from_menu)

        if registryDict is not None:
            self.openProjectWithRegistryDict(registryDict)

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
