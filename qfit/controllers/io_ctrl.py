import sys
import os
import gc
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
from qfit.utils.load_reg_dict import parseRegDict
import qfit.settings as settings

from typing import (
    TYPE_CHECKING,
    Union,
    Dict,
    Any,
    Optional,
    List,
    Callable,
    Tuple,
)

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import MeasDataType, MeasDataSet
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

    Relevant UI elements:
    - menu button
    - menu widget

    Relevant model:
    - hilbertspace
    - measurement data importer

    Parameters
    ----------
    parent : QObject
        parent object
    menuButton : QPushButton
        button to open the menu
    menuUi : MenuWidget
        the menu widget
    registry : Registry
        the registry object
    mainWindow : MainWindow
        the main window
    fullReplaceHS : Callable[[HilbertSpace], None]
        function to replace the HilbertSpace object for all components
        in qfit.
    fullReplaceMeasData : Callable[[List[MeasurementDataType]], None]
        function to replace the measurement data for all components in qfit
    fullDynamicalInit : Callable[[], None]
        function to reinitialize the dynamical elements in the main window,
        once the fullReplaceHS and fullReplaceMeasData are called.
    """

    def __init__(
        self,
        parent: QObject,
        models: Tuple["MeasDataSet", "Registry"],
        views: Tuple["QPushButton", "MenuWidget", "MainWindow"],
        fullReplaceHS: Callable[["HilbertSpace"], None],
    ):
        super().__init__(parent)
        self.measDataSet, self.registry = models
        self.menuButton, self.menu, self.mainWindow = views
        self.fullReplaceHS = fullReplaceHS
        self._appClosed = False

        self.setConnects()

    def replaceHS(self, hilbertspace: "HilbertSpace"):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views. HilbertSpace is used
        to help reload the app if it is not provided in the newProject function.

        Parameters
        ----------
        hilbertspace : HilbertSpace
            the HilbertSpace object
        """
        self.hilbertSpace = hilbertspace

    def setConnects(self):
        """
        Connect the buttons to the corresponding functions, including
        - toggle
        - quit (via menu or "x" button)
        - open
        - new
        - save
        - save as
        """
        self.menuButton.clicked.connect(self.menu.toggle)

        self.menu.ui.menuQuitButton.clicked.connect(self.mainWindow.close)
        self.menu.ui.menuQuitButton.clicked.connect(self.menu.toggle)
        self.menu.ui.menuOpenButton.clicked.connect(self.openFile)
        self.menu.ui.menuNewButton.clicked.connect(self.newProject)
        self.menu.ui.menuSaveButton.clicked.connect(self.saveFile)
        self.menu.ui.menuSaveAsButton.clicked.connect(self.saveFileAs)
        self.mainWindow.closeWindow.connect(self.closeByMainWindow)

    # properties ##############################################################
    @property
    def appClosed(self):
        return self._appClosed

    @appClosed.setter
    def appClosed(self, value: bool):
        raise ValueError("appClosed can't be set externally and is read-only.")

    # load data from file #####################################################
    def _registryDictFromDialog(
        self,
        home=None,
        window_initialized=False,
    ) -> Union[Dict[str, Any], None]:
        """
        Open a dialog to select a file, then read the registryDict from the file.

        Parameters
        ----------
        home : str
            the home directory to start the dialog
        windowInitialized : bool
            whether the main window is initialized. If not, the app will close
            if the user cancels the dialog.
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
                    self._closeApp()
                    raise StopExecution
                else:
                    return None

            registryDict = Registry.dictFromFile(fileName)

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

    # open ####################################################################

    # save ####################################################################
    def _saveProject(
        self,
        home=None,
        save_as: bool = False,
    ):
        """
        Open a dialog to select a file, then save the project to the file.

        Parameters
        ----------
        home : str
            the home directory to start the dialog
        save_as : bool
            whether to save the project as a new file
        """
        if not self.measDataSet.importFinished:
            raise ValueError("Import is not finished.")

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
        self.forceSaveAs(fileName)

    def forceSaveAs(self, fileName: str):
        """
        Regardless of whether the project is saved or not before, save the project
        as a new file indicated by `fileName`.

        Parameters
        ----------
        fileName : str
            the file name to save the project
        """
        self.mainWindow.projectFile = fileName
        self.registry.exportPkl(fileName)

    # quit / close ############################################################
    def _closeApp(self):
        """
        Close the window.
        """
        self._appClosed = True

        if settings.EXECUTED_IN_IPYTHON:
            self.mainWindow.blockSignals(True)
            self.mainWindow.close()
            self.mainWindow.blockSignals(False)
            self.mainWindow.deleteLater()
            # self.mainWindow.destroy()
            gc.collect()
            # raise StopExecution
        else:
            sys.exit()

    def _saveAndCloseApp(self, save_as: bool = False):
        """Save the extracted data and calibration information to file, then exit the
        application."""
        success = self._saveProject(save_as=save_as)
        if not success:
            return
        self._closeApp()

    def closeAppAfterSaving(self) -> bool:
        """
        Close the app after asking the user whether to save the changes.

        Returns
        -------
        bool
            whether the app is closed
        """
        # first, if the project is open from a file, check the registry dict of the old file
        # with that obtained from the current session, if something changed, ask the user
        # whether to save the changes
        if self.mainWindow.projectFile is not None:
            registryDict = copy.deepcopy(self.registry.exportDict())
            registryDictFromFile = copy.deepcopy(
                Registry.dictFromFile(self.mainWindow.projectFile)
            )
            assert registryDictFromFile is not None, "File not found"

            # parse the registry dicts
            registryDictFromFile = parseRegDict(registryDictFromFile)

            # remove HilbertSpace and file name from these dicts
            # we don't want to compare these two entries
            # because the HilbertSpace object does not have a proper __eq__ method
            # and the file name may be different for similar projects
            registryDict.pop("HilbertSpace")
            registryDictFromFile.pop("HilbertSpace")
            registryDict.pop("MainWindow._projectFile")
            registryDictFromFile.pop("MainWindow._projectFile")

            # compare the two dicts
            if registryDict != registryDictFromFile:
                self.mainWindow.unsavedChanges = True
            else:
                self.mainWindow.unsavedChanges = False

        else:
            self.mainWindow.unsavedChanges = True

        if self.mainWindow.unsavedChanges and self.measDataSet.importFinished:
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
                self._saveAndCloseApp(save_as=self.mainWindow.projectFile is None)
                return True
            elif reply == QMessageBox.Discard:
                self._closeApp()
                return True
            else:  # reply == QMessageBox.Cancel
                return False

        else:
            self._closeApp()
            return True

    # slots ###################################################################
    @Slot()
    def newProject(
        self,
        __value=None,
        from_menu: bool = True,
        hilbertSpace: Optional["HilbertSpace"] = None,
        measurementFileName: Optional[str | List[str]] = None,
        deepcopy: bool = False,
    ):
        """
        Open a dialog to select a measurement file, then create a new project.
        It is a slot for the new project button in the menu.

        Parameters
        ----------
        from_menu : bool
            whether the function is called from the menu. If Truem the menu
            will be closed after the function is called.
        hilbertSpace : HilbertSpace
            the HilbertSpace object
        measurementFileName : str
            the measurement file name
        deepcopy : bool
            whether to use a deepcopy of the HilbertSpace object, instead of
            referencing the original HilbertSpace object. The latter option
            updates the original HilbertSpace object during any prefit / fit
            operations.
        """
        if from_menu and self.menu.isVisible():
            self.menu.toggle()

        # load or re-use the HilbertSpace object
        if hilbertSpace is not None:
            self.hilbertSpace = hilbertSpace
        if deepcopy:
            self.hilbertSpace = copy.deepcopy(self.hilbertSpace)
        self.fullReplaceHS(self.hilbertSpace)

        # feed the measurement data to the measDataSet
        openWindow = self.measDataSet.insertRow(measurementFileName)
        # set the focus to the main window after opening a file
        self.mainWindow.activateWindow()

        if not openWindow:
            # the only reason is user canceled the dialog
            if not from_menu:
                self._closeApp()
                # raise StopExecution
            else:
                # do nothing
                return

    @Slot()
    def openFile(
        self,
        __value=None,
        from_menu: bool = True,
        fileName: Optional[str] = None,
        deepcopy: bool = False,
    ):
        """
        Open a dialog to select a project file, then open the project.
        It is a slot for the open file button in the menu.

        Parameters
        ----------
        from_menu : bool
            whether the function is called from the menu. If Truem the menu
            will be closed after the function is called.
        fileName : str
            the project file name
        deepcopy : bool
            whether to use a deepcopy of the HilbertSpace object, instead of
            referencing the original HilbertSpace object. Even when the HilbertSpace
            object is serialized, the non-deepcopied HilbertSpace object may still
            cause correlated updates to the original HilbertSpace object / other
            HilbertSpace objects.
        """
        if from_menu and self.menu.isVisible():
            self.menu.toggle()

        # check if file exists
        if fileName is not None:
            if not os.path.isfile(fileName):
                raise FileNotFoundError(f"File '{fileName}' does not exist.")

        if fileName is None:
            registryDict = self._registryDictFromDialog(window_initialized=from_menu)
        else:
            registryDict = Registry.dictFromFile(fileName)
            if registryDict is None:
                raise FileNotFoundError(f"Can't load file '{fileName}'.")

        if registryDict is not None:
            # load the hilbertspace and measurementData
            parsedDict = parseRegDict(registryDict)
            hilbertspace, measurementData = (
                parsedDict["HilbertSpace"],
                parsedDict["MeasDataSet.data"],
            )
            if deepcopy:
                hilbertspace = copy.deepcopy(hilbertspace)
            # update the dynamical elements in the main window (i.e. load from the registry
            # the r entries)
            self.fullReplaceHS(hilbertspace)
            self.measDataSet.loadDataSet(measurementData)

            # update the rest of the registry (i.e. those entries with r+)
            self.registry.setByDict(parsedDict)

            self.mainWindow.unsavedChanges = False

    @Slot()
    def saveFile(self):
        """Save the extracted data and calibration information to file."""
        self._saveProject(save_as=False)

        if self.menu.isVisible():
            self.menu.toggle()

    @Slot()
    def saveFileAs(self):
        """Save the extracted data and calibration information to file."""
        self._saveProject(save_as=True)

        if self.menu.isVisible():
            self.menu.toggle()

    @Slot()
    def closeByMainWindow(self, event):
        """
        When user click the "x" button, mainWinow will emit the closeWindow
        signal and this function will be called. It will ask the user whether
        to save the changes before closing the app.
        """
        status = self.closeAppAfterSaving()

        if status:
            event.accept()
        else:
            event.ignore()
