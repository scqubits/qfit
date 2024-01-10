# mainwindow.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import copy
import sys
import os
from functools import partial
from typing import TYPE_CHECKING, Dict, Tuple, Union, List, Any

import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np

from scqubits.core.hilbert_space import HilbertSpace

from PySide6.QtCore import (
    QPoint,
    QRect,
    QSize,
    Qt,
    Slot,
    QCoreApplication,
    QThreadPool,
    QEvent,
    Signal,
)
from PySide6.QtGui import QColor, QMouseEvent, Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStyle,
    QCheckBox,
    QSizePolicy,
)

import qfit.core.app_state as appstate
from qfit.models.calibration_data import CalibrationData
from qfit.widgets.calibration import CalibrationView
from qfit.core.app_state import State
from qfit.utils.helpers import (
    transposeEach,
    clearChildren,
    executed_in_ipython,
    StopExecution,
    y_snap,
)
from qfit.models.extracted_data import ActiveExtractedData, AllExtractedData
from qfit.models.measurement_data import MeasurementDataType
from qfit.controllers.tagging import TaggingCtrl
from qfit.controllers.help_tooltip import HelpButtonCtrl
from qfit.settings import color_dict
from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

# pre-fit
from qfit.models.quantum_model_parameters import (
    QuantumModelSliderParameter,
    QuantumModelParameterSet,
    QuantumModelFittingParameter,
)
from qfit.models.numerical_spectrum_data import CalculatedSpecData
from qfit.models.numerical_model import QuantumModel
from qfit.widgets.foldable_widget import FoldableWidget
from qfit.widgets.grouped_sliders import (
    LabeledSlider,
    GroupedWidgetSet,
    SPACING_BETWEEN_GROUPS,
)
from qfit.widgets.foldable_table import (
    FoldableTable,
    MinMaxItems,
    FittingParameterItems,
)

# fit
from qfit.models.fit import NumericalFitting

# message
from qfit.models.status_result_data import Result

# registry
from qfit.models.registry import Registry, RegistryEntry, Registrable

# menu controller
from qfit.controllers.io_menu import IOCtrl

if TYPE_CHECKING:
    from qfit.widgets.calibration import CalibrationLineEdit

mpl.rcParams["toolbar"] = "None"


# metaclass: solve the incompatibility and make the mainWindow registrable
class CombinedMeta(type(QMainWindow), type(Registrable)):
    pass


class MainWindow(QMainWindow, Registrable, metaclass=CombinedMeta):
    """Class for the main window of the app."""

    ui: Ui_MainWindow
    # ui_menu: Ui_MenuWidget

    measurementData: MeasurementDataType
    activeDataset: ActiveExtractedData
    allDatasets: AllExtractedData
    taggingCtrl: TaggingCtrl

    calibrationData: CalibrationData
    calibrationView: CalibrationView
    rawLineEdits: Dict[str, "CalibrationLineEdit"]
    mapLineEdits: Dict[str, "CalibrationLineEdit"]
    calibrationButtons: Dict[str, QPushButton]
    calibrationStates: Dict[str, State]

    axes: mpl.axes.Axes
    cidCanvas: int
    offset: Union[None, QPoint]

    optInitialized: bool = False

    unsavedChanges: bool
    registry: Registry
    _projectFile: Union[str, None] = None

    def __init__(
        self, measurementData: MeasurementDataType, hilbertspace: HilbertSpace
    ):
        # self.hilbertspace = hilbertspace

        # ResizableFramelessWindow.__init__(self)
        QMainWindow.__init__(self)
        self.openFromIPython = executed_in_ipython()
        self.disconnectCanvas = False  # used to temporarily switch off canvas updates
        self.setFocusPolicy(Qt.StrongFocus)
        self.offset = None

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # fix visibility of collapsible panels
        # self.ui.xyzDataGridFrame.setVisible(False)
        # self.ui.filterQFrame.setVisible(False)

        self.ui_menu = MenuWidget(parent=self)

        self.setShadows()
        self.ui.verticalSnapButton.setAutoExclusive(False)

        self.uiPagesConnects()
        self.uiGrouping()

        # calibration
        self.setupUICalibration()
        self.calibrationData = CalibrationData()
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())

        self.x_snap_mode = False
        self.mousedat = None

        self.setupUIPlotOptions()

        self.measurementData = measurementData
        self.initializeExtractedData()
        self.staticExtractedDataConnects(hilbertspace)

        self.dynamicalMeasurementDataSetupConnects(hilbertspace)
        self.uiDataLoadConnects()

        # setup mpl canvas
        self.uiColorScaleConnects()
        self.uiCalibrationConnects()
        self.uiCanvasControlConnects()
        self.uiMplCanvasConnects()
        # self.ui.mplFigureCanvas.selectOn()

        # prefit: controller, two models and their connection to view (sliders)
        self.prefitDynamicalElementsBuild(hilbertspace)
        self.prefitStaticElementsBuild()

        # fit
        self.fitDynamicalElementsBuild()
        self.fitStaticElementsBuild()

        # help button
        self.helpButtonConnects()

        # register all the data
        self.registry = Registry()

        # controller for menu
        self.ioMenuCtrl = IOCtrl(
            ui_Menu=self.ui_menu,
            registry=self.registry,
            mainWindow=self,
        )

        # status bar
        # self.statusBar().showMessage("Ready")

    # ui grouping ######################################################
    ####################################################################
    def uiGrouping(self):
        """
        Group the UI elements into different groups, making it easier to
        hand over to the controller.
        """

        # Extract: Labling
        self.uiLabelBoxes = {
            "bare": self.ui.tagBareGroupBox,
            "dressed": self.ui.tagDressedGroupBox,
        }
        self.uiLabelRadioButtons = {
            "bare": self.ui.tagDispersiveBareRadioButton,
            "dressed": self.ui.tagDispersiveDressedRadioButton,
            "no tag": self.ui.noTagRadioButton,
        }
        self.uiBareLabelInputs = {
            "initial": self.ui.initialStateLineEdit,
            "final": self.ui.finalStateLineEdit,
            "photons": self.ui.phNumberBareSpinBox,
        }
        self.uiDressedLabelInputs = {
            "initial": self.ui.initialStateSpinBox,
            "final": self.ui.finalStateSpinBox,
            "photons": self.ui.phNumberDressedSpinBox,
        }

        return 

    # help button and gif tooltip ######################################
    ####################################################################
    def helpButtonConnects(self):
        self.helpButtons = {
            "calibration": self.ui.calibrationHelpPushButton,
            "fit": self.ui.fitHelpPushButton,
            "fitResult": self.ui.fitResultHelpPushButton,
            "prefitResult": self.ui.prefitResultHelpPushButton,
            "numericalSpectrumSettings": self.ui.numericalSpectrumSettingsHelpPushButton,
        }
        self.helpButtonCtrl = HelpButtonCtrl(self.helpButtons)

    # calibration, data, plot setup ####################################
    ####################################################################
    def staticExtractedDataConnects(self, hilbertspace: HilbertSpace):
        self.uiExtractedDataConnects()
        self.uiExtractedDataControlConnects()

        self.taggingCtrl = TaggingCtrl(
            hilbertspace.subsystem_count,
            (self.allDatasets, self.activeDataset),
            (self.uiLabelBoxes, self.uiLabelRadioButtons, self.uiBareLabelInputs, self.uiDressedLabelInputs)
        )

    def dynamicalMeasurementDataSetupConnects(self, hilbertspace: HilbertSpace):
        self.measurementData.setupUICallbacks(
            self.dataCheckBoxCallbacks, self.plotRangeCallback
        )

        # inform the use of the bare transition label
        self.ui.bareLabelOrder.setText(
            "Labels ordered by: <br>"  # Three space to align with the label title
            + ", ".join([subsys.id_str for subsys in hilbertspace.subsystem_list])
        )

        self.uiMeasurementDataOptionsConnects()

        self.setupUIXYZComboBoxes()
        self.uiXYZComboBoxesConnects()

    def recoverFromExtractedData(self):
        if self.extractedData is not None:
            self.allDatasets.dataNames = self.extractedData.datanames
            self.allDatasets.assocDataList = transposeEach(self.extractedData.datalist)
            self.allDatasets.assocTagList = self.extractedData.tag_data
            self.calibrationData.setCalibration(
                *self.extractedData.calibration_data.allCalibrationVecs()
            )

            self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())
            self.activeDataset._data = self.allDatasets.currentAssocItem()
            self.taggingCtrl.setTagInView(self.allDatasets.currentTagItem())
            self.allDatasets.layoutChanged.emit()
            self.activeDataset.layoutChanged.emit()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.offset = None
        super().mouseReleaseEvent(event)

    def setShadows(self):
        for button in [
            self.ui.newRowButton,
            self.ui.deleteRowButton,
            self.ui.clearAllButton,
            self.ui.horizontalSnapButton,
            self.ui.verticalSnapButton,
            self.ui.calibrateX1Button,
            self.ui.calibrateX2Button,
            self.ui.calibrateY1Button,
            self.ui.calibrateY2Button,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

        for button in [
            self.ui.zoomViewButton,
            self.ui.resetViewButton,
            self.ui.panViewButton,
            self.ui.selectViewButton,
            self.ui.swapXYButton,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

    def setupUICalibration(self):
        """For the interface that enables calibration of data with respect to x and y axis, group QLineEdit elements
        and the corresponding buttons in dicts. Set up a dictionary mapping calibration labels to the corresponding
        State choices. Finally, set up an instance of CalibrationData and CalibrationView.
        """
        self.rawLineEdits = {
            "X1": self.ui.rawX1LineEdit,
            "X2": self.ui.rawX2LineEdit,
            "Y1": self.ui.rawY1LineEdit,
            "Y2": self.ui.rawY2LineEdit,
        }
        self.mapLineEdits = {
            "X1": self.ui.mapX1LineEdit,
            "X2": self.ui.mapX2LineEdit,
            "Y1": self.ui.mapY1LineEdit,
            "Y2": self.ui.mapY2LineEdit,
        }
        self.calibrationButtons = {
            "X1": self.ui.calibrateX1Button,
            "X2": self.ui.calibrateX2Button,
            "Y1": self.ui.calibrateY1Button,
            "Y2": self.ui.calibrateY2Button,
        }
        self.calibrationStates = {
            "X1": State.CALIBRATE_X1,
            "X2": State.CALIBRATE_X2,
            "Y1": State.CALIBRATE_Y1,
            "Y2": State.CALIBRATE_Y2,
        }

        self.calibrationView = CalibrationView(self.rawLineEdits, self.mapLineEdits)

    def setupUIPlotOptions(self):
        self.dataCheckBoxCallbacks = {
            "topHatFilter": self.ui.topHatCheckBox.isChecked,
            "waveletFilter": self.ui.waveletCheckBox.isChecked,
            "edgeFilter": self.ui.edgeFilterCheckBox.isChecked,
            "bgndSubtractX": self.ui.bgndSubtractXCheckBox.isChecked,
            "bgndSubtractY": self.ui.bgndSubtractYCheckBox.isChecked,
            "logColoring": self.ui.logScaleCheckBox.isChecked,
        }

    def plotRangeCallback(self):
        val1 = self.ui.rangeSliderMin.value() / 100.0
        val2 = self.ui.rangeSliderMax.value() / 100.0
        min_val = min(val1, val2)
        max_val = max(val1, val2)
        return [min_val, max_val]

    def initializeExtractedData(self):
        """Set up the main class instances holding the data extracted from placing
        markers on the canvas. The AllExtractedData instance holds all data, whereas the
        ActiveExtractedData instance holds data of the currently selected data set."""
        self.activeDataset = ActiveExtractedData()
        self.activeDataset.setAdaptiveCalibrationFunc(
            self.calibrationData.adaptiveConversionFunc
        )
        # self.ui.dataTableView.setModel(self.activeDataset)

        self.allDatasets = AllExtractedData()
        self.allDatasets.setCalibrationFunc(self.calibrationData.calibrateDataset)
        self.ui.datasetListView.setModel(self.allDatasets)

    def setupUIXYZComboBoxes(self):
        zDataNames = list(self.measurementData.zCandidates.keys())
        self.ui.zComboBox.clear()
        self.ui.zComboBox.addItems(zDataNames)
        self.ui.zComboBox.setCurrentText(self.measurementData.currentZ.name)
        self.setupXYDataBoxes()

    def uiPagesConnects(self):
        """Connect the UI elements for switching between the different pages."""

        # page 0: Calibrate (previously Extract)
        self.ui.modeSelectButton.clicked.connect(lambda: self._switchToPage(0))
        # page 1: Extract & Tag (previously Tag)
        self.ui.modeTagButton.clicked.connect(lambda: self._switchToPage(1))
        # page 2: Prefit
        self.ui.modePrefitButton.clicked.connect(lambda: self._switchToPage(2))
        # page 3: Fit
        self.ui.modeFitButton.clicked.connect(lambda: self._switchToPage(3))

        # when clicked parameter export button, switch to the desired page
        self.ui.exportToFitButton.clicked.connect(lambda: self._switchToPage(3))
        self.ui.exportToPrefitButton.clicked.connect(lambda: self._switchToPage(2))

    @Slot()
    def _switchToPage(self, page: int):
        # update MSE when switching between fit / pre-fit page
        if self.ui.pagesStackedWidget.currentIndex() == 2 and page == 3:
            self.ui.mseLabel_2.setText(self.ui.mseLabel.text())
        elif self.ui.pagesStackedWidget.currentIndex() == 3 and page == 2:
            self.ui.mseLabel.setText(self.ui.mseLabel_2.text())

        # switch to the desired page
        self.ui.pagesStackedWidget.setCurrentIndex(page)
        self.ui.bottomStackedWidget.setCurrentIndex(page)

        # set the corresponding button to checked
        self.ui.modeSelectButton.setChecked(False)
        self.ui.modeTagButton.setChecked(False)
        self.ui.modePrefitButton.setChecked(False)
        self.ui.modeFitButton.setChecked(False)
        if page == 0:
            self.ui.modeSelectButton.setChecked(True)
        elif page == 1:
            self.ui.modeTagButton.setChecked(True)
        elif page == 2:
            self.ui.modePrefitButton.setChecked(True)
        elif page == 3:
            self.ui.modeFitButton.setChecked(True)

        self.updateMatchingModeAndCursor()
        self.updatePlot()

    def uiExtractedDataConnects(self):
        """Make connections for changes in extracted data."""

        # whenever a row is inserted or removed, select the current row
        # this connection should be put before the connection of layoutChanged
        # as the latter will be triggered by the former
        self.allDatasets.rowsInserted.connect(
            lambda: self.ui.datasetListView.selectItem(self.allDatasets.currentRow)
        )
        self.allDatasets.rowsRemoved.connect(
            lambda: self.ui.datasetListView.selectItem(self.allDatasets.currentRow)
        )

        # Whenever the data layout in the ActiveExtractedData changes, update
        # the corresponding AllExtractedData data; this includes the important
        # event of adding extraction points to the ActiveExtractedData
        self.activeDataset.layoutChanged.connect(
            lambda: self.ui.datasetListView.model().updateAssocData(
                newData=self.activeDataset.all()
            )
        )

        # If data in the TableView is changed manually through editing,
        # the 'dataChanged' signal will be emitted. The following connects the signal
        # to an update in th data stored in the AllExtractedData
        self.activeDataset.dataChanged.connect(
            lambda topLeft, bottomRight: self.ui.datasetListView.model().updateAssocData(
                newData=self.activeDataset.all()
            )
        )

        # Whenever the AllExtractedData changes layout - for example, due to
        # switching from one existing data set to another one, this connection will
        # ensure that the TableView will be updated with the correct data
        self.allDatasets.layoutChanged.connect(
            lambda: self.activeDataset.setAllData(
                newData=self.allDatasets.currentAssocItem()
            )
        )

        # Whenever data sets are added or removed from the ListView, this ensures
        # that the canvas display is updated.
        self.allDatasets.layoutChanged.connect(self.updatePlot)

        # Each time the data set is changed on ListView/Model by clicking a data set,
        # the data in ActiveExtractedData is updated to reflect the new selection.
        self.ui.datasetListView.clicked.connect(
            lambda: self.activeDataset.setAllData(
                newData=self.allDatasets.currentAssocItem()
            )
        )

        # A new selection of a data set item in ListView is accompanied by an update
        # of the canvas to show the appropriate plot of selected points
        self.ui.datasetListView.clicked.connect(
            lambda: self.updatePlot(initialize=False)
        )

        # Whenever a new selection of data set is made, update the matching mode and the cursor
        self.allDatasets.layoutChanged.connect(self.updateMatchingModeAndCursor)
        self.ui.datasetListView.clicked.connect(self.updateMatchingModeAndCursor)

    def uiMeasurementDataOptionsConnects(self):
        """Connect the UI elements related to display of data"""
        self.ui.topHatCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.waveletCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.edgeFilterCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.bgndSubtractXCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.bgndSubtractYCheckBox.toggled.connect(lambda x: self.updatePlot())

    def uiColorScaleConnects(self):
        """Connect the color scale related UI elements."""
        # Toggling the loc scale check box prompts replotting.
        self.ui.logScaleCheckBox.toggled.connect(lambda x: self.updatePlot())

        # Changes in the color map dropdown menu prompt replotting.
        self.ui.colorComboBox.activated.connect(lambda x: self.updatePlot())

        # Ensure that a change in the range slider positions cause an update of the plot.
        self.ui.rangeSliderMin.valueChanged.connect(lambda x: self.updatePlot())
        self.ui.rangeSliderMax.valueChanged.connect(lambda x: self.updatePlot())

    def uiCalibrationConnects(self):
        """Connect UI elements for data calibration."""
        self.ui.calibratedCheckBox.toggled.connect(self.toggleCalibration)

        for label in self.calibrationButtons:
            self.calibrationButtons[label].clicked.connect(
                partial(self.calibrate, label)
            )

        for lineEdit in list(self.rawLineEdits.values()) + list(
            self.mapLineEdits.values()
        ):
            lineEdit.editingFinished.connect(self.updateCalibration)

    def uiCanvasControlConnects(self):
        """Connect the UI buttons for reset, zoom, and pan functions of the matplotlib canvas."""
        self.ui.resetViewButton.clicked.connect(self.ui.mplFigureCanvas.resetView)
        self.ui.zoomViewButton.clicked.connect(self.toggleZoom)
        self.ui.panViewButton.clicked.connect(self.togglePan)
        self.ui.selectViewButton.clicked.connect(self.toggleSelect)
        self.ui.swapXYButton.clicked.connect(self.swapXY)

    def uiExtractedDataControlConnects(self):
        """Connect buttons for inserting and deleting a data set, or clearing all data sets"""
        # update the backend model
        self.ui.newRowButton.clicked.connect(self.allDatasets.newRow)
        self.ui.deleteRowButton.clicked.connect(self.allDatasets.removeCurrentRow)
        self.ui.clearAllButton.clicked.connect(self.allDatasets.onClearClicked)

    def uiDataLoadConnects(self):
        self.allDatasets.loadFromRegistrySignal.signal.connect(self.extractedDataSetup)

    def uiXYZComboBoxesConnects(self):
        self.ui.zComboBox.activated.connect(self.zDataUpdate)
        self.ui.xComboBox.activated.connect(self.xAxisUpdate)
        self.ui.yComboBox.activated.connect(self.yAxisUpdate)

    def updateMatchingModeAndCursor(self):
        """
        Callback for updating the matching mode and the cursor
        """
        # matching mode
        if (
            self.allDatasets
            and self.allDatasets.currentRow != 0
            and len(self.allDatasets.assocDataList[0][0]) > 0
            and self.ui.horizontalSnapButton.isChecked()
            and (appstate.state not in list(self.calibrationStates.values()))
        ):
            self.x_snap_mode = True
        else:
            self.x_snap_mode = False

        strXY = None
        # cursor
        if self.ui.modeTagButton.isChecked() and self.ui.selectViewButton.isChecked():
            horizOn, vertOn = True, True
        else:
            horizOn, vertOn = False, False
        if (
            appstate.state == self.calibrationStates["X1"]
            or appstate.state == self.calibrationStates["X2"]
        ):
            horizOn, vertOn = False, True
            strXY = "X"
        elif (
            appstate.state == self.calibrationStates["Y1"]
            or appstate.state == self.calibrationStates["Y2"]
        ):
            horizOn, vertOn = True, False
            strXY = "Y"

        self.ui.mplFigureCanvas.select_crosshair(
            axis_snap_mode=strXY,
            x_snap_mode=self.x_snap_mode,
            horizOn=horizOn,
            vertOn=vertOn,
        )

    def calibrationButtonIsChecked(self):
        """
        Check if any of the calibration buttons is checked
        """
        for label in self.calibrationButtons:
            if self.calibrationButtons[label].isChecked():
                return True
        return False

    def uiMplCanvasConnects(self):
        """Set up the matplotlib canvas and start monitoring for mouse click events in the canvas area."""
        self.axes = self.ui.mplFigureCanvas.canvas.figure.subplots()
        self.updatePlot(initialize=True)
        self.cidCanvas = self.axes.figure.canvas.mpl_connect(
            "button_press_event", self.canvasClickMonitoring
        )
        self.ui.horizontalSnapButton.toggled.connect(self.updateMatchingModeAndCursor)
        # connects the updateMatchingModeAndCursor with calibration buttons
        for label in self.calibrationButtons:
            self.calibrationButtons[label].toggled.connect(
                self.updateMatchingModeAndCursor
            )
        self.updateMatchingModeAndCursor()
        self.ui.mplFigureCanvas.set_callback_for_extracted_data(self.allDatasets)
        self.cidMove = self.axes.figure.canvas.mpl_connect(
            "motion_notify_event", self.canvasMouseMonitoring
        )

    def setupXYDataBoxes(self):
        self.ui.xComboBox.clear()
        xDataNames = list(self.measurementData.currentXCompatibles.keys())
        self.ui.xComboBox.addItems(xDataNames)
        self.ui.xComboBox.setCurrentText(self.measurementData.currentX.name)

        self.ui.yComboBox.clear()
        yDataNames = list(self.measurementData.currentYCompatibles.keys())
        self.ui.yComboBox.addItems(yDataNames)
        self.ui.yComboBox.setCurrentText(self.measurementData.currentY.name)

    @Slot()
    def toggleSelect(self):
        if appstate.state != State.SELECT:
            appstate.state = State.SELECT
            self.ui.mplFigureCanvas.selectOn(
                showCrosshair=self.ui.modeTagButton.isChecked()
            )

    @Slot()
    def toggleZoom(self):
        if appstate.state != "ZOOM":
            appstate.state = State.ZOOM
            self.ui.mplFigureCanvas.zoomView()

    @Slot()
    def togglePan(self):
        if appstate.state != "PAN":
            appstate.state = State.PAN
            self.ui.mplFigureCanvas.panView()

    def line_select_callback(self, eclick, erelease):
        """
        Callback for line selection.

        *eclick* and *erelease* are the press and release events.
        """
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        # print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")
        # print(f" The buttons you used were: {eclick.button} {erelease.button}")

    @Slot()
    def canvasClickMonitoring(self, event):
        """Main loop for acting on mouse events occurring in the canvas area."""
        if event.xdata is None or event.ydata is None:
            return

        # calibration mode
        if self.ui.modeSelectButton.isChecked():
            for calibrationLabel in ["X1", "X2", "Y1", "Y2"]:
                data = event.xdata if (calibrationLabel[0] == "X") else event.ydata

                if appstate.state == self.calibrationStates[calibrationLabel]:
                    # turn off the highlighting of the button
                    self._highlightCaliButton(
                        self.calibrationButtons[calibrationLabel], reset=True
                    )
                    # update the raw line edits by the value of the clicked point
                    self.rawLineEdits[calibrationLabel].setText(str(data))
                    self.rawLineEdits[calibrationLabel].home(False)
                    # highlight the map line edit
                    self.mapLineEdits[calibrationLabel].selectAll()
                    self.mapLineEdits[calibrationLabel].setFocus()
                    self.ui.selectViewButton.setChecked(True)
                    self.ui.mplFigureCanvas.selectOn()
                    self.rawLineEdits[calibrationLabel].editingFinished.emit()
                    return

        # select mode
        if self.ui.modeTagButton.isChecked() and appstate.state == State.SELECT:
            current_data = self.activeDataset.all()
            if self.x_snap_mode:
                x1y1 = np.asarray([self.closest_line(event.xdata), event.ydata])
            else:
                x1y1 = np.asarray([event.xdata, event.ydata])
                # turn on the horizontal snap automatically, if the user turned it off
                self.ui.horizontalSnapButton.setChecked(True)
            for index, x2y2 in enumerate(current_data.transpose()):
                if self.isRelativelyClose(x1y1, x2y2):
                    self.activeDataset.removeColumn(index)
                    self.updatePlot()
                    return
            if self.ui.verticalSnapButton.isChecked():
                x_list = self.measurementData.currentX.data
                y_list = self.measurementData.currentY.data
                z_data = self.measurementData.currentZ.data
                # calculate half index range as 5x linewidth
                linewidth = 0.02  # GHz
                half_y_range = linewidth * 5
                try:
                    snapped_y1 = y_snap(
                        x_list=x_list,
                        y_list=y_list,
                        z_data=z_data,
                        user_selected_xy=x1y1,
                        half_y_range=half_y_range,
                        mode="lorentzian",
                    )
                    x1y1_snapped = np.asarray([x1y1[0], snapped_y1])
                    self.activeDataset.append(*x1y1_snapped)
                except RuntimeError:
                    self.activeDataset.append(*x1y1)
            else:
                self.activeDataset.append(*x1y1)
            self.updatePlot()

    @Slot()
    def canvasMouseMonitoring(self, event):
        self.axes.figure.canvas.flush_events()
        if not self.x_snap_mode:
            return

        if event.xdata is None or event.ydata is None:
            return

    @Slot()
    def updatePlot(self, initialize: bool = False, **kwargs):
        """Update the current plot of measurement data and markers of selected data
        points."""
        if self.disconnectCanvas:
            return

        # If this is not the first time of plotting, store the current axes limits and
        # clear the graph.
        if not initialize:
            xlim = self.axes.get_xlim()
            ylim = self.axes.get_ylim()
        self.axes.clear()

        # Set the matplotlib colormap according to the selection in the dropdown menu.
        colorStr = self.ui.colorComboBox.currentText()
        cross_color = color_dict[colorStr]["Cross"]
        line_color = color_dict[colorStr]["line"]
        scatter_color = color_dict[colorStr]["Scatter"]
        cmap = copy.copy(getattr(cm, colorStr))
        cmap.set_bad(color="black")

        # plot the background data
        self.measurementData.canvasPlot(self.axes, cmap=cmap, rasterized=True)

        # plot the numerically calculated spectrum
        if not initialize:
            self.spectrumData.canvasPlot(self.axes)

        # If there are any extracted data points in the currently active data set, show
        # those via a scatter plot.
        if self.ui.modeTagButton.isChecked():
            if not self.activeDataset.isEmpty():
                dataXY = self.activeDataset.all()
                self.axes.scatter(
                    dataXY[0],
                    dataXY[1],
                    c=scatter_color,
                    marker=r"$\odot$",
                    s=130,
                    alpha=0.3,
                )
            for data in self.allDatasets.assocDataList:
                if data.size > 0 and data is not self.activeDataset.all():
                    self.axes.scatter(
                        data[0],
                        data[1],
                        c=scatter_color,
                        marker=r"$\times$",
                        s=70,
                        alpha=0.23,
                    )
            if not self.allDatasets.isEmpty():
                dataXY = self.activeDataset.all()
                self.axes.scatter(
                    dataXY[0],
                    dataXY[1],
                    c=scatter_color,
                    marker=r"$\odot$",
                    s=130,
                    alpha=0.3,
                )
        elif not self.ui.modeSelectButton.isChecked():
            if not self.allDatasets.isEmpty():
                dataXY = self.allDatasets.allDataSorted(
                    applyCalibration=False,
                    concat_data=True,
                )

                self.axes.scatter(
                    dataXY[:, 0],
                    dataXY[:, 1],
                    c=scatter_color,
                    marker=r"$\odot$",
                    s=130,
                    alpha=0.3,
                )

        plotted_data = []
        # line_data = self.allDatasets.assocDataList[0]
        x_list = self.allDatasets.distinctSortedXValues()
        for x_value in x_list:
            self.axes.axvline(
                x_value,
                c=line_color,
                alpha=0.3,
            )

        # if toggle calibration is checked, change the xlabel to the scqubits parameter
        # name and ylabel to energy in GHz; also apply changes to the ticks.
        if self.ui.calibratedCheckBox.isChecked():
            # xlabel = <swept_parameter> (<sysstem id string>)
            xlabel = (
                list(list(self.sweepParameterSet.values())[0].keys())[0]
                + " "
                + "("
                + list(list(self.sweepParameterSet.values())[0].values())[
                    0
                ].parent.id_str
                + ")"
            )
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylabel("energy [GHz]")
            # update ticks to reflect the calibration
            # get the current labels and locations
            xlocs, xticklabels = self.axes.get_xticks(), self.axes.get_xticklabels()
            ylocs, yticklabels = self.axes.get_yticks(), self.axes.get_yticklabels()
            # update the labels using the calibration function
            # notice that the label positions are obtained from x(y)ticklabels which
            # are text objects.
            # results are rounded to 2 decimals
            xticklabels = np.round(
                self.calibrationData.calibrateDataset(
                    array=np.array(
                        [
                            [float(xticklabel.get_position()[0]), 0]
                            for xticklabel in xticklabels
                        ]
                    ).T,
                    calibration_axis="x",
                )[0, :],
                decimals=2,
            )
            yticklabels = np.round(
                self.calibrationData.calibrateDataset(
                    array=np.array(
                        [
                            [0, float(yticklabel.get_position()[1])]
                            for yticklabel in yticklabels
                        ]
                    ).T,
                    calibration_axis="y",
                )[1, :],
                decimals=2,
            )
            self.axes.set_xticks(xlocs, xticklabels)
            self.axes.set_yticks(ylocs, yticklabels)
        else:
            self.axes.set_xlabel(self.measurementData.currentX.name)
            self.axes.set_ylabel(self.measurementData.currentY.name)

        # Make sure that new axes limits match the old ones.
        if not initialize:
            self.axes.set_xlim(xlim)
            self.axes.set_ylim(ylim)

        self.axes.figure.canvas.draw()
        self.ui.mplFigureCanvas.x_snap_mode = self.x_snap_mode
        self.ui.mplFigureCanvas.set_callback_for_extracted_data(self.allDatasets)

    def _highlightCaliButton(self, button: QPushButton, reset: bool = False):
        """Highlight the button by changing its color."""
        if reset:
            button.setStyleSheet("")
        else:
            button.setStyleSheet("QPushButton {background-color: #6c278c}")

    def _resetHighlightButtons(self):
        """Reset the highlighting of all calibration buttons."""
        for label in self.calibrationButtons:
            self._highlightCaliButton(self.calibrationButtons[label], reset=True)

    @Slot()
    def calibrate(self, calibrationLabel: str):
        """
        Mouse click on one of the calibration buttons prompts switching to
        calibration mode. Mouse cursor crosshair is adjusted and canvas waits for
        click setting calibration point x or y component.
        Besides, the button is highlighted.
        """
        appstate.state = self.calibrationStates[calibrationLabel]
        # button highlighting
        self._resetHighlightButtons()
        self._highlightCaliButton(self.calibrationButtons[calibrationLabel])
        # mpl canvas mode & cursor
        self.updateMatchingModeAndCursor()
        # notice that this line overwrites the crosshair selection in updateMatchingModeAndCursor
        self.ui.mplFigureCanvas.calibrateOn()

    @Slot()
    def updateCalibration(self):
        """Transfer new calibration data from CalibrationView over to calibrationData
        instance. If the model is currently applying the calibration, then emit
        signal to rewrite the table."""
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())
        if self.calibrationData.applyCalibration:
            self.activeDataset.layoutChanged.emit()

    @Slot()
    def toggleCalibration(self):
        """If calibration check box is changed, toggle the calibration status of the
        calibrationData. Also induce change at the level of the displayed data of
        selected points."""
        self.calibrationData.toggleCalibration()
        # update the plot to reflect the change in calibration label
        self.updatePlot()
        self.activeDataset.toggleCalibratedView()

    @Slot(int)
    def zDataUpdate(self, itemIndex: int):
        self.measurementData.setCurrentZ(itemIndex)
        self.setupXYDataBoxes()
        self.updatePlot(initialize=True)

    @Slot(int)
    def xAxisUpdate(self, itemIndex: int):
        self.measurementData.setCurrentX(itemIndex)
        self.updatePlot(initialize=True)

    @Slot(int)
    def yAxisUpdate(self, itemIndex: int):
        self.measurementData.setCurrentY(itemIndex)
        self.updatePlot(initialize=True)

    @Slot()
    def swapXY(self):
        self.disconnectCanvas = True
        self.measurementData.swapXY()
        self.setupXYDataBoxes()

        self.allDatasets.swapXY()
        self.allDatasets.layoutChanged.emit()

        xBgndSub = self.ui.bgndSubtractXCheckBox.checkState()
        yBgndSub = self.ui.bgndSubtractYCheckBox.checkState()

        self.ui.bgndSubtractXCheckBox.setCheckState(yBgndSub)
        self.ui.bgndSubtractYCheckBox.setCheckState(xBgndSub)

        rawx1 = self.rawLineEdits["X1"].value()
        rawx2 = self.rawLineEdits["X2"].value()
        rawy1 = self.rawLineEdits["Y1"].value()
        rawy2 = self.rawLineEdits["Y2"].value()
        mapx1 = self.mapLineEdits["X1"].value()
        mapx2 = self.mapLineEdits["X2"].value()
        mapy1 = self.mapLineEdits["Y1"].value()
        mapy2 = self.mapLineEdits["Y2"].value()
        self.rawLineEdits["X1"].setText(str(rawy1))
        self.rawLineEdits["Y1"].setText(str(rawx1))
        self.rawLineEdits["X2"].setText(str(rawy2))
        self.rawLineEdits["Y2"].setText(str(rawx2))
        self.mapLineEdits["X1"].setText(str(mapy1))
        self.mapLineEdits["Y1"].setText(str(mapx1))
        self.mapLineEdits["X2"].setText(str(mapy2))
        self.mapLineEdits["Y2"].setText(str(mapx2))
        self.updateCalibration()

        self.disconnectCanvas = False
        self.updatePlot(initialize=True)

    def isRelativelyClose(self, x1y1: np.ndarray, x2y2: np.ndarray):
        """Check whether the point x1y1 is relatively close to x2y2, given the current
        field of view on the canvas."""
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        xrange = xmax - xmin
        yrange = ymax - ymin
        x1y1 = x1y1 / [xrange, yrange]
        x2y2 = x2y2 / [xrange, yrange]
        distance = np.linalg.norm(x1y1 - x2y2)
        if distance < 0.025:
            return True
        return False

    def closest_line(self, xdat):
        all_x_list = self.allDatasets.distinctSortedXValues()
        allxdiff = {np.abs(xdat - i): i for i in all_x_list}
        return allxdiff[min(allxdiff.keys())]

    # Pre-fit ##########################################################
    # ##################################################################
    def prefitDynamicalElementsBuild(self, hilbertspace: HilbertSpace):
        self.sliderParameterSet = QuantumModelParameterSet("sliderParameterSet")
        self.sweepParameterSet = QuantumModelParameterSet("sweepParameterSet")
        self.quantumModel = QuantumModel(hilbertspace)

        self.quantumModel.addParametersToParameterSet(
            self.sweepParameterSet,
            parameter_usage="sweep",
            included_parameter_type=["ng", "flux"],
        )

        self.prefitIdentifySweepParameters()
        self.prefitSlidersInserts()
        self.prefitMinMaxInserts()
        self.prefitSliderParamConnects()
        self.prefitSubsystemComboBoxLoads()
        self.prefitQuantumModelOptionsConnects()
        self.setUpPrefitRunConnects()

    def prefitStaticElementsBuild(self):
        self.prefitResult = Result()
        self.spectrumData = CalculatedSpecData()
        self.setUpPrefitResultConnects()
        self.prefitGeneralOptionsConnects()

    def prefitIdentifySweepParameters(self):
        """
        Model init: identify sweep parameters

        sweepParameterSet -init-> sliderParameterSet
        """
        # check how many sweep parameters are found and create sliders
        # for the remaining parameters
        param_types = set(self.sweepParameterSet.exportAttrDict("param_type").values())
        if len(self.sweepParameterSet) == 0:
            print(
                "No sweep parameter (ng / flux) is found in the HilbertSpace "
                "object. Please check your quantum model."
            )
            self.close()
        elif len(self.sweepParameterSet) == 1:
            # only one sweep parameter is found, so we can create sliders
            # for the remaining parameters
            self.quantumModel.addParametersToParameterSet(
                self.sliderParameterSet,
                parameter_usage="slider",
                excluded_parameter_type=(
                    ["cutoff", "truncated_dim", "l_osc"]
                    + [list(param_types)[0]]  # exclude the sweep parameter
                ),
            )
        elif len(self.sweepParameterSet) == 2 and param_types == set(["flux", "ng"]):
            # a flux and ng are detected in the HilbertSpace object
            # right now, we assume that the flux is always swept in this case
            self.quantumModel.addParametersToParameterSet(
                self.sliderParameterSet,
                parameter_usage="slider",
                excluded_parameter_type=(["flux", "cutoff", "truncated_dim", "l_osc"]),
            )
        else:
            print(
                "Unfortunately, the current version of qfit does not support "
                "multiple sweep parameters (flux / ng). This feature will be "
                "available in the next release."
            )
            self.close()

    @Slot()
    def onParameterChange(self, slider_or_fit_parameter_set: QuantumModelParameterSet):
        """
        Model & View updates
        """
        self.quantumModel.updateCalculation(
            slider_or_fit_parameter_set=slider_or_fit_parameter_set,
            sweep_parameter_set=self.sweepParameterSet,
            spectrum_data=self.spectrumData,
            calibration_data=self.calibrationData,
            extracted_data=self.allDatasets,
            prefit_result=self.prefitResult,
        )

        # TODO: move to a separate connection: model --> view
        self.updatePlot()

    @Slot()
    def onPrefitPlotClicked(self):
        """
        Model & View updates
        """
        self.quantumModel.sweep2SpecNMSE(
            slider_or_fit_parameter_set=self.sliderParameterSet,
            sweep_parameter_set=self.sweepParameterSet,
            spectrum_data=self.spectrumData,
            extracted_data=self.allDatasets,
            calibration_data=self.calibrationData,
            result=self.prefitResult,
        )

        # TODO: move to a separate connection: model --> view
        self.updatePlot()

    def prefitSlidersInserts(self):
        """
        View init: pre-fit sliders

        Insert a set of sliders for the prefit parameters according to the parameter set
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        clearChildren(self.ui.prefitScrollAreaWidget)

        # create a QWidget for the scrollArea and set a layout for it
        prefitScrollLayout = self.ui.prefitScrollAreaWidget.layout()

        # set the alignment of the entire prefit scroll layout
        prefitScrollLayout.setAlignment(Qt.AlignTop)

        # generate the slider set
        self.sliderSet = GroupedWidgetSet(
            widget_class=LabeledSlider,
            init_kwargs={"label_value_position": "left_right"},
            columns=1,
            parent=self.ui.prefitScrollAreaWidget,
        )

        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]

            self.sliderSet.addGroupedWidgets(
                group_name,
                list(para_dict.keys()),
            )

        prefitScrollLayout.addWidget(self.sliderSet)

        # add a spacing between the sliders and the min max table
        prefitScrollLayout.addSpacing(SPACING_BETWEEN_GROUPS)

    def prefitMinMaxInserts(self):
        """
        View init: pre-fit min max table
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        clearChildren(self.ui.prefitMinmaxScrollAreaWidget)

        # create a QWidget for the minmax scroll area and set a layout for it
        prefitMinmaxScrollLayout = self.ui.prefitMinmaxScrollAreaWidget.layout()

        # set the alignment of the entire prefit minmax scroll layout
        prefitMinmaxScrollLayout.setAlignment(Qt.AlignTop)

        self.minMaxTable = FoldableTable(
            MinMaxItems,
            paramNumPerRow=1,
            groupNames=list(self.sliderParameterSet.parentNameByObj.values()),
        )
        self.minMaxTable.setCheckable(False)
        self.minMaxTable.setChecked(False)

        # insert parameters
        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]

            for para_name in para_dict.keys():
                self.minMaxTable.insertParams(group_name, para_name)

        # add the minmax table to the scroll area
        foldable_widget = FoldableWidget("RANGES OF SLIDERS", self.minMaxTable)
        prefitMinmaxScrollLayout.addWidget(foldable_widget)

        # default to fold the table
        foldable_widget.toggle()

    def prefitSliderParamConnects(self):
        """
        View --> model: slider --> parameter
        """
        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]

            for para_name, para in para_dict.items():
                para: QuantumModelSliderParameter
                labeled_slider: LabeledSlider = self.sliderSet[group_name][para_name]
                minMax: MinMaxItems = self.minMaxTable.params[group_name][para_name]

                para.setupUICallbacks(
                    labeled_slider.slider.value,
                    labeled_slider.slider.setValue,
                    labeled_slider.value.text,
                    labeled_slider.setValue,
                    minMax.minValue.text,
                    minMax.minValue.setText,
                    minMax.maxValue.text,
                    minMax.maxValue.setText,
                )

                # synchronize slider and box
                labeled_slider.sliderValueChangedConnect(para.sliderValueToBox)
                labeled_slider.valueTextChangeConnect(para.boxValueToSlider)

                # format the user's input
                labeled_slider.value.editingFinished.connect(para.onBoxEditingFinished)
                minMax.minValue.editingFinished.connect(para.onMinEditingFinished)
                minMax.maxValue.editingFinished.connect(para.onMaxEditingFinished)

                para.setParameterForParent()

    def prefitParamModelConnects(self):
        """
        View --> model: slider --> parameter
        TODO: This should be param --> model rather than slider --> model.
        model --> model: parameter --> numerical model
        model --> view: numerical model --> prefit plot
        TODO: should be able to seprate the connection

        It complete a flow of information from the slider to the model.
        """
        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.parentNameByObj[key]
            for para_name, para in para_dict.items():
                labeled_slider: LabeledSlider = self.sliderSet[group_name][para_name]

                # connect to the controller to update the spectrum
                labeled_slider.editingFinishedConnect(
                    lambda: self.onParameterChange(self.sliderParameterSet)
                )

    def prefitSubsystemComboBoxLoads(self):
        """
        View init: pre-fit subsystem combo box
        loading the subsystem names to the combo box (drop down menu)
        """
        # clear the existing items and temporarily disable the signal
        self.ui.subsysComboBox.blockSignals(True)
        self.ui.subsysComboBox.clear()

        subsys_name_list = [
            QuantumModelParameterSet.parentSystemNames(subsys)
            for subsys in self.quantumModel.hilbertspace.subsystem_list[::-1]
        ]
        for subsys_name in subsys_name_list:
            self.ui.subsysComboBox.insertItem(0, subsys_name)

        # enable the signal
        self.ui.subsysComboBox.blockSignals(False)

    def setUpPrefitResultConnects(self):
        """
        Model --> View: pre-fit result
        connect the prefit result to the relevant UI textboxes; whenever there is
        a change in the UI, reflect in the UI text change
        """
        status_type_ui_setter = lambda: self.ui.label_46.setText(
            self.prefitResult.displayed_status_type
        )
        status_text_ui_setter = lambda: self.ui.statusTextLabel.setText(
            self.prefitResult.status_text
        )
        mse_change_ui_setter = lambda: self.ui.mseLabel.setText(
            self.prefitResult.displayed_MSE
        )

        self.prefitResult.setupUISetters(
            status_type_ui_setter=status_type_ui_setter,
            status_text_ui_setter=status_text_ui_setter,
            mse_change_ui_setter=mse_change_ui_setter,
        )

    def prefitQuantumModelOptionsConnects(self):
        """
        View --> model: pre-fit options

        TODO: Should be able to combine with prefitGeneralOptionsConnects
        """
        # connect the prefit options to the controller
        self.quantumModel.setupPlotUICallbacks(
            subsystemNameCallback=self.ui.subsysComboBox.currentText,
            initialStateCallback=self.ui.initStateLineEdit.text,
            photonsCallback=self.ui.prefitPhotonSpinBox.value,
            evalsCountCallback=self.ui.evalsCountLineEdit.text,
            pointsAddCallback=self.ui.pointsAddLineEdit.text,
        )

    def prefitGeneralOptionsConnects(self):
        """
        View --> model: numerical model options
        model --> view: numerical model --> prefit plot
        TODO: should be able to seprate the connection
        TODO: Should be able to combine with prefitQuantumModelOptionsConnects

        Set up the connects for the prefit options for UI:
        1. subsystem combo box
        2. initial state line edit
        3. photons spin box
        4. evals count line edit
        5. points add line edit
        """

        # set line edit property:
        self.ui.initStateLineEdit.setTupleLength(
            self.quantumModel.hilbertspace.subsystem_count
        )

        # when change those numbers, update the spectrum data using the
        # existing sweep
        self.ui.subsysComboBox.currentIndexChanged.connect(self.onPrefitPlotClicked)
        self.ui.initStateLineEdit.editingFinished.connect(self.onPrefitPlotClicked)
        self.ui.prefitPhotonSpinBox.valueChanged.connect(
            lambda: print("current photons: ", self.ui.prefitPhotonSpinBox.value())
        )
        self.ui.prefitPhotonSpinBox.valueChanged.connect(self.onPrefitPlotClicked)

        # when change those numbers, update the sweep and then update the spectrum
        self.ui.evalsCountLineEdit.editingFinished.connect(
            lambda: self.onParameterChange(self.sliderParameterSet)
        )
        self.ui.pointsAddLineEdit.editingFinished.connect(
            lambda: self.onParameterChange(self.sliderParameterSet)
        )

    def setUpPrefitRunConnects(self):
        """
        View --> model: run sweep
        model --> view: pre-fit plot
        TODO: should be able to seprate the connection

        Set up the connects for the prefit run for UI:
        1. autorun checkbox
        2. run (or "plot") button
        """
        # connect the autorun checkbox callback
        self.quantumModel.setupAutorunCallbacks(
            autorun_callback=self.ui.autoRunCheckBox.isChecked,
        )
        self.ui.autoRunCheckBox.setChecked(True)
        # connect the run button callback to the generation and run of parameter sweep
        # notice that parameter update is done in the slider connects
        # TODO: here is a bug, since the parameter update is done in the slider connects,
        # if parameters are updated due to the fitting step, and the fitting result parameters
        # are not imported to the prefit parameters, then the HilbertSpace is still using the
        # fit parameters; if user want to plot with prefit parameters, clicking the plot button
        # in the prefit will not update the parameters based on the sliders.
        self.ui.plotButton.clicked.connect(self.onPrefitPlotClicked)

    # Fit ##############################################################
    # ##################################################################

    def fitDynamicalElementsBuild(self):
        self.fitParameterSet = QuantumModelParameterSet("fitParameterSet")
        self.quantumModel.addParametersToParameterSet(
            self.fitParameterSet,
            parameter_usage="fit",
            excluded_parameter_type=["ng", "flux", "cutoff", "truncated_dim", "l_osc"],
        )
        self.fitTableInserts()
        self.fitTableConnects()

    def fitStaticElementsBuild(self):
        self.threadpool = QThreadPool()
        self.numericalFitting = NumericalFitting()
        self.setupFitConnects()
        self.fittingCallbackConnects()
        self.fitPushButtonConnects()

        self.fitResult = Result()
        self.setUpFitResultConnects()

    def setupFitConnects(self):
        self.numericalFitting.setupUICallbacks(
            self.ui.optimizerComboBox.currentText,
            self.ui.tolLineEdit.text,
        )

    def fitTableInserts(self):
        """
        Insert a set of tables for the fitting parameters
        """

        fitScrollWidget = self.ui.fitScrollAreaWidget

        # remove the existing widgets, if we somehow want to rebuild the sliders
        clearChildren(fitScrollWidget)
        if fitScrollWidget.layout() is None:
            fitScrollLayout = QVBoxLayout(fitScrollWidget)
        else:
            fitScrollLayout = fitScrollWidget.layout()

        # configure this layout
        self.ui.fitScrollArea.setStyleSheet(f"background-color: rgb(33, 33, 33);")
        fitScrollWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # create an empty table with just group names
        self.fitTableSet = FoldableTable(
            FittingParameterItems,
            paramNumPerRow=1,
            groupNames=list(self.fitParameterSet.parentNameByObj.values()),
        )

        # insert parameters
        for key, para_dict in self.fitParameterSet.items():
            group_name = self.fitParameterSet.parentNameByObj[key]

            for para_name in para_dict.keys():
                self.fitTableSet.insertParams(group_name, para_name)

        fitScrollLayout.addWidget(self.fitTableSet)

    def fittingParameterLoad(self, source: QuantumModelParameterSet):
        """
        Load the initial value, min, and max from the source parameter set
        """
        init_value_dict = source.exportAttrDict("value")
        self.fitParameterSet.loadAttrDict(init_value_dict, "initValue")
        self.fitParameterSet.loadAttrDict(init_value_dict, "value")
        max_value_dict = {
            key: (value * 1.2 if value > 0 else value * 0.8)
            for key, value in init_value_dict.items()
        }
        self.fitParameterSet.loadAttrDict(max_value_dict, "max")
        min_value_dict = {
            key: (value * 0.8 if value > 0 else value * 1.2)
            for key, value in init_value_dict.items()
        }
        self.fitParameterSet.loadAttrDict(min_value_dict, "min")

    @Slot()
    def _setupOptimization(self):
        """
        Run optimization step 1: setup the optimization using various parameters
        """

        self.optInitialized = self.numericalFitting.setupOptimization(
            self.fitParameterSet,
            self.quantumModel.MSEByParameters,
            self.allDatasets,
            self.sweepParameterSet,
            self.calibrationData,
            self.fitResult,
        )

    @Slot()
    def _backgroundOptimization(self):
        """
        Run optimization step 2: run the optimization in the background
        """
        if not self.optInitialized:
            return

        self.ui.fitButton.setEnabled(False)
        self.sliderSet.setEnabled(False)

        # start the optimization
        self.threadpool.start(self.numericalFitting)

    @Slot()
    def _onOptFinished(self):
        print("Optimization finished")

        self.ui.fitButton.setEnabled(True)
        self.sliderSet.setEnabled(True)

        # the numericalFitting object will be deleted after background running
        # so we need to create a new one and connect the signals again
        self.numericalFitting = NumericalFitting()
        self.setupFitConnects()
        self.fittingCallbackConnects()

        # should be used after re-create the numericalFitting object
        # (for the optimization failing case)
        self.onParameterChange(self.fitParameterSet)
        self.updatePlot()

    def fittingCallbackConnects(self):
        """
        when the optimization is finished, send a signal that triggers
        the `_onOptFinished` function
        """
        self.numericalFitting.signals.optFinished.connect(self._onOptFinished)

    def fitPushButtonConnects(self):
        """
        Connect the buttons for
        1. run fit
        2. parameters transfer: prefit to fit
        3. parameters transfer: fit to prefit
        4. parameters transfer: fit result to fit
        """
        # setup the optimization
        self.ui.fitButton.clicked.connect(self._setupOptimization)

        # connect the fit button to the fitting function
        self.ui.fitButton.clicked.connect(self._backgroundOptimization)

        # the prefit parameter export
        self.ui.exportToFitButton.clicked.connect(
            lambda: self.fittingParameterLoad(self.sliderParameterSet)
        )

        # the prefit parameter transfer
        self.ui.pushButton_2.clicked.connect(
            lambda: self.fittingParameterLoad(self.fitParameterSet)
        )

        # the prefit parameter import
        # first update the slider parameter set, then perform the necessary changes
        # as slider parameter changes
        self.ui.exportToPrefitButton.clicked.connect(
            lambda: self.sliderParameterSet.update(self.fitParameterSet)
        )
        self.ui.exportToPrefitButton.clicked.connect(
            lambda: self.onParameterChange(self.sliderParameterSet)
        )

    def fitTableConnects(self):
        """
        Connect the tables (ui) to the model - two parameter sets
        """

        for key, para_dict in self.fitParameterSet.items():
            group_name = self.fitParameterSet.parentNameByObj[key]

            for para_name, para in para_dict.items():
                para: QuantumModelFittingParameter
                single_row: FittingParameterItems = self.fitTableSet.params[group_name][
                    para_name
                ]

                # connect the UI and the model
                para.setupUICallbacks(
                    single_row.initialValue.text,
                    single_row.initialValue.setText,
                    single_row.resultValue.text,
                    single_row.resultValue.setText,
                    single_row.minValue.text,
                    single_row.minValue.setText,
                    single_row.maxValue.text,
                    single_row.maxValue.setText,
                    single_row.fixCheckbox.isChecked,
                    single_row.fixCheckbox.setChecked,
                )

                # format the user's input
                single_row.initialValue.editingFinished.connect(
                    para.onInitValueEditingFinished
                )
                single_row.minValue.editingFinished.connect(para.onMinEditingFinished)
                single_row.maxValue.editingFinished.connect(para.onMaxEditingFinished)

                para.initialize()

    def setUpFitResultConnects(self):
        """
        connect the prefit result to the relevant UI textboxes;
        whenever there is a change in the UI, reflect in the UI text change
        """
        status_type_ui_setter = lambda: self.ui.label_49.setText(
            self.fitResult.displayed_status_type
        )
        status_text_ui_setter = lambda: self.ui.statusTextLabel_2.setText(
            self.fitResult.status_text
        )
        mse_change_ui_setter = lambda: self.ui.mseLabel_2.setText(
            self.fitResult.displayed_MSE
        )

        self.fitResult.setupUISetters(
            status_type_ui_setter=status_type_ui_setter,
            status_text_ui_setter=status_text_ui_setter,
            mse_change_ui_setter=mse_change_ui_setter,
        )

    # Save Location & Window Title #####################################
    # ##################################################################
    @property
    def projectFile(self):
        return self._projectFile

    @projectFile.setter
    def projectFile(self, value):
        self._projectFile = value

        windowTitle = "qfit" if value is None else f"qfit - {os.path.basename(value)}"
        self.setWindowTitle(windowTitle)

    # IO ###############################################################
    # ##################################################################

    attrToRegister: List[str] = [
        "projectFile",
    ]

    def registerAll(self):
        """
        After registering the models,
        Register the rest attribute of the mainWindow.
        """
        registryDict = {
            attr: self._toRegistryEntry(attr) for attr in self.attrToRegister
        }

        return registryDict

    def register(self):
        """
        register the entire app
        """
        # clear the registry
        self.registry.clear()

        # special registry
        self.registry.register(self.quantumModel.hilbertspace)
        self.registry.register(self.measurementData)
        self.registry.register(self.calibrationData)
        self.registry.register(self.allDatasets)

        # parameters
        self.registry.register(self.sliderParameterSet)
        self.registry.register(self.fitParameterSet)
        self.registry.register(self.sweepParameterSet)

        # main window
        self.registry.register(self)

    def initializeDynamicalElements(
        self,
        hilbertspace: HilbertSpace,
        measurementData: MeasurementDataType,
    ):
        # here, the measurementData is a instance of MeasurementData, which is
        # regenerated from the data file
        self.measurementData = measurementData
        self.calibrationData.resetCalibration()
        self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())

        self.allDatasets.blockSignals(True)
        self.allDatasets.removeAll()
        self.allDatasets.blockSignals(False)

        self.dynamicalMeasurementDataSetupConnects(hilbertspace)
        self.uiDataLoadConnects()
        self.setupUIXYZComboBoxes()

        self.prefitDynamicalElementsBuild(hilbertspace)
        self.fitDynamicalElementsBuild()

        self.updatePlot(initialize=True)

        self.register()

        self.raise_()

    def closeEvent(self, event):
        """
        Override the original class method to add a confirmation dialog before
        closing the application. Will be triggered when the user clicks the "X"
        or call the close() method.
        """
        try:
            status = self.ioMenuCtrl.closeApp()

            if status:
                event.accept()
            else:
                event.ignore()
        except AttributeError:
            # the GUI is partially initialized and don't have the ioMenuCtrl
            event.accept()

    @Slot()
    def extractedDataSetup(self, initdata):
        """
        Recover extracted data from initdata, and emit changes to the view
        """
        # recover the allDatasets model
        datanames = initdata["datanames"]
        datalist = initdata["datalist"]
        tag_data = initdata["taglist"]
        self.allDatasets.dataNames = datanames
        self.allDatasets.assocDataList = transposeEach(datalist)
        self.allDatasets.assocTagList = tag_data
        # set calibration
        # this might worth a separate signal/slot, because the initialDynamicalElements only
        # initialize the calibration data, and it does not recover the progress on the previous
        # calibration.
        self.calibrationData.setCalibration(*self.calibrationData.allCalibrationVecs())
        self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())
        # set active dataset
        self.activeDataset._data = self.allDatasets.currentAssocItem()
        self.allDatasets.layoutChanged.emit()
        self.activeDataset.layoutChanged.emit()

    def resizeAndCenter(self, maxSize: QSize):
        newSize = QSize(maxSize.width() * 0.9, maxSize.height() * 0.9)
        maxRect = QRect(QPoint(0, 0), maxSize)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, newSize, maxRect)
        )

    # event filter and save state ######################################
    # ##################################################################
    # def install_event_filters(self):
    #     self.installEventFilter(self)
    #     for widget in self.findChildren(QWidget):
    #         widget.installEventFilter(self)

    # def eventFilter(self, source, event):
    #     if (
    #         event.type() == QEvent.Type.KeyPress
    #     ):  # Or other event types you're interested in
    #         self.unsavedChanges = True
    #     return super().eventFilter(source, event)
