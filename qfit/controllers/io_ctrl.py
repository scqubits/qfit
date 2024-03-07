import sys
import os
import numpy as np
import copy

from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QFileDialog,
)


from qfit.models.registry import Registry
from qfit.widgets.menu import MenuWidget
from qfit.utils.helpers import StopExecution
from qfit.io_utils.measurement_file_readers import readMeasurementFile
from qfit.utils.helpers import executed_in_ipython

from typing import (
    TYPE_CHECKING, Union, Dict, Any, Optional, List,
    Callable,
)

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import (
        MeasurementDataType,
    )
    from scqubits.core.hilbert_space import HilbertSpace


class IOCtrl(QObject):
    """
    It is a companion class to the Fit, helping handling the IO operations.
    This controller handles the menu bar and related IO operations, including:
    - new project
    - open file
    - save file
    - save file as
    - close app

    It will run the register() when created.

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
        parent: QObject,
        menuButton: QPushButton,
        menuUi: MenuWidget,
        registry: Registry,
        mainWindow: "MainWindow",  
        fullDynmicalInit: Callable[["HilbertSpace", List["MeasurementDataType"]], None],
    ):
        super().__init__(parent)
        self.menuButton = menuButton
        self.menu = menuUi
        self.registry = registry
        self.mainWindow = mainWindow
        self.fullDynamicalInit = fullDynmicalInit

        self.setConnects()

    def dynamicalInit(self, hilbertspace: "HilbertSpace"):
        """
        Dynamically initialize the main window with the hilbertspace and measurement data.
        """
        self.hilbertSpace = hilbertspace

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
        self.menuButton.clicked.connect(self.menu.toggle)

        self.menu.ui.menuQuitButton.clicked.connect(self.mainWindow.close)
        self.menu.ui.menuOpenButton.clicked.connect(self.openFile)
        self.menu.ui.menuNewButton.clicked.connect(self.newProject)
        self.menu.ui.menuSaveButton.clicked.connect(self.saveFile)
        self.menu.ui.menuSaveAsButton.clicked.connect(self.saveFileAs)
        self.mainWindow.closeWindow.connect(self.closeByMainWindow)

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
                    self._closeAppAfterSaving()
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
                    self._closeAppAfterSaving()
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

    # quit / close ############################################################
    def _closeAppAfterSaving(self) -> bool:
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
            # we don't want to compare these two entries
            # because the HilbertSpace object does not have a proper __eq__ method
            # and the file name may be different for similar projects
            registryDict.pop("HilbertSpace")
            registryDictFromFile.pop("HilbertSpace")
            registryDict.pop("projectFile")
            registryDictFromFile.pop("projectFile")

            # compare the two dicts
            if registryDict != registryDictFromFile:
                self.mainWindow.unsavedChanges = True
            else:
                self.mainWindow.unsavedChanges = False

        else:
            self.mainWindow.unsavedChanges = True

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
                self.saveAndCloseApp(
                    save_as = self.mainWindow.projectFile is None
                )
                return True
            elif reply == QMessageBox.Discard:
                self._closeApp()
                return True
            else:  # reply == QMessageBox.Cancel
                self.menu.toggle()
                return False

        else:
            self._closeApp()
            return True
        
    def _closeApp(self):
        if executed_in_ipython():
            print("IOCtrl.closeApp")
            self.mainWindow.close()
            self.mainWindow.deleteLater()
            self.mainWindow.destroy()
            # raise StopExecution
        else:
            sys.exit()

    # slots ###################################################################
    @Slot()
    def newProject(
        self, 
        __value=None, 
        from_menu: bool = True, 
        hilbertSpace: Optional["HilbertSpace"] = None,
        measurementFileName: Optional[str] = None,
    ):
        """
        Open a dialog to select a measurement file, then create a new project
        """
        if from_menu:
            self.menu.toggle()

        # ask for a measurement file from dialog
        if measurementFileName is None:
            measurementData = self._measurementDataFromDialog(window_initialized=from_menu)
            if measurementData is None:
                # dialog will handle this and we just do nothing
                return
        else:
            measurementData = self._measurementDataFromFile(
                measurementFileName
            )
            if measurementData is None:
                raise FileNotFoundError(f"Can't load file '{measurementFileName}'.")

        if hilbertSpace is not None:
            self.hilbertSpace = hilbertSpace

        self.fullDynamicalInit(self.hilbertSpace, [measurementData])

    @Slot()
    def openFile(
        self, 
        __value=None, 
        from_menu: bool = True,
        fileName: Optional[str] = None,
    ):
        """
        Open a dialog to select a project file, then open the project
        """
        if from_menu:
            self.menu.toggle()

        if fileName is None:
            registryDict = self._registryDictFromDialog(
                window_initialized=from_menu
            )
        else:
            registryDict = self._registryDictFromFile(fileName)
            if registryDict is None:
                raise FileNotFoundError(f"Can't load file '{fileName}'.")

        if registryDict is not None:
            # load the hilbertspace and measurementData
            hilbertspace = registryDict["HilbertSpace"]
            measurementData = registryDict["measDataSet.data"]

            # update the dynamical elements in the main window (i.e. load from the registry
            # the r entries)
            self.fullDynamicalInit(
                hilbertspace,
                measurementData,
            )

            # update the rest of the registry (i.e. those entries with r+)
            self.registry.setByDict(registryDict)

            self.mainWindow.unsavedChanges = False

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
    def saveAndCloseApp(self, save_as: bool = False):
        """Save the extracted data and calibration information to file, then exit the
        application."""
        success = self._saveProject(save_as=save_as)
        if not success:
            return
        self._closeApp()

    @Slot()
    def closeByMainWindow(self, event):
        print("IO ctrl close called")
        status = self._closeAppAfterSaving()

        if status:
            event.accept()
        else:
            event.ignore()
