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
from typing import TYPE_CHECKING, Dict, Tuple, Union, List, Any, Literal

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

from qfit.models.calibration_data import CalibrationData
from qfit.widgets.calibration import CalibrationView
from qfit.utils.helpers import (
    transposeEach,
    clearChildren,
    executed_in_ipython,
    StopExecution,
)
from qfit.models.measurement_data import MeasurementDataType
from qfit.controllers.help_tooltip import HelpButtonCtrl
from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

# paging:
from qfit.views.paging import PageView

# extract
from qfit.models.extracted_data import ActiveExtractedData, AllExtractedData
from qfit.controllers.extracting import ExtractingCtrl
from qfit.views.extracting import ExtractingView

# status bar
from qfit.models.status import StatusModel
from qfit.controllers.status import StatusCtrl
from qfit.views.status_bar import StatusBarView

# pre-fit
from qfit.models.quantum_model_parameters import (
    QuantumModelSliderParameter,
    QuantumModelParameterSet,
    QuantumModelFittingParameter,
)
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

# plot
from qfit.controllers.plotting import PlottingCtrl

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

    status: StatusModel

    optInitialized: bool = False

    unsavedChanges: bool
    registry: Registry
    _projectFile: Union[str, None] = None

    def __init__(
        self, measurementData: MeasurementDataType, hilbertspace: HilbertSpace
    ):
        QMainWindow.__init__(self)
        self.openFromIPython = executed_in_ipython()
        self.setFocusPolicy(Qt.StrongFocus)

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setShadows()
        self.ui.verticalSnapButton.setAutoExclusive(False)

        # navigation
        self.ui_menu = MenuWidget(parent=self)
        self.pagingMVCInits()

        # calibration
        self.calibrationMVCInits()
        self.uiCalibrationConnects()

        # extract
        self.extractingMVCInits(hilbertspace)
        self.extractingCtrl.dynamicalInit()

        # prefit: controller, two models and their connection to view (sliders)
        self.prefitDynamicalElementsBuild(hilbertspace)
        self.prefitStaticElementsBuild()

        # fit
        self.fitDynamicalElementsBuild()
        self.fitStaticElementsBuild()

        # plot, mpl canvas
        self.measurementData = measurementData
        self.plottingMVCInits()
        self.plottingCtrl.dynamicalInit(
            self.measurementData, self.quantumModel
        )

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
        self.statusMVCInits()

    # ui setup #########################################################
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

    # plot #############################################################
    ####################################################################  
    def plottingMVCInits(self):
        # ui grouping
        self.measComboBoxes = {
            "x": self.ui.xComboBox,
            "y": self.ui.yComboBox,
            "z": self.ui.zComboBox,
        }
        self.measPlotSettings = {
            "topHat": self.ui.topHatCheckBox,
            "wavelet": self.ui.waveletCheckBox,
            "edge": self.ui.edgeFilterCheckBox,
            "bgndX": self.ui.bgndSubtractXCheckBox,
            "bgndY": self.ui.bgndSubtractYCheckBox,
            "log": self.ui.logScaleCheckBox,
            "min": self.ui.rangeSliderMin,
            "max": self.ui.rangeSliderMax,
            "color": self.ui.colorComboBox,
        }
        self.canvasTools = {
            "reset": self.ui.resetViewButton,
            "zoom": self.ui.zoomViewButton,
            "pan": self.ui.panViewButton,
            "select": self.ui.selectViewButton,
            "snapX": self.ui.horizontalSnapButton,
            "snapY": self.ui.verticalSnapButton,
        }

        self.plottingCtrl = PlottingCtrl(
            self.ui.mplFigureCanvas,
            (
                self.measurementData, self.calibrationData,
                self.allDatasets, self.activeDataset,
                self.quantumModel, self.sweepParameterSet,
            ), (
                self.measComboBoxes, self.measPlotSettings, self.ui.swapXYButton,
                self.canvasTools, self.calibrationButtons, self.ui.calibratedCheckBox, 
                self.pageView
            ),
        )  

    # menu #############################################################
    ####################################################################
    def pagingMVCInits(self):
        """
        Set up an instance of PageView.
        """
        self.pageButtons = {
            "calibrate": self.ui.modeSelectButton,
            "extract": self.ui.modeTagButton,
            "prefit": self.ui.modePrefitButton,
            "fit": self.ui.modeFitButton,
        }
        self.dataExportButtons = {
            "prefit": self.ui.exportToPrefitButton,
            "fit": self.ui.exportToFitButton,
        }
        self.pageStackedWidgets = {
            "center": self.ui.pagesStackedWidget,
            "bottom": self.ui.bottomStackedWidget,
        }

        self.pageView = PageView(
            self.pageButtons, self.dataExportButtons, self.pageStackedWidgets
        )


    # calibration ####################################
    ####################################################################
    def calibrationMVCInits(self):
        """
        Set up an instance of CalibrationData and CalibrationView.
        """
        # ui grouping
        self.rawLineEdits = {
            "CALI_X1": self.ui.rawX1LineEdit,
            "CALI_X2": self.ui.rawX2LineEdit,
            "CALI_Y1": self.ui.rawY1LineEdit,
            "CALI_Y2": self.ui.rawY2LineEdit,
        }
        self.mapLineEdits = {
            "CALI_X1": self.ui.mapX1LineEdit,
            "CALI_X2": self.ui.mapX2LineEdit,
            "CALI_Y1": self.ui.mapY1LineEdit,
            "CALI_Y2": self.ui.mapY2LineEdit,
        }
        self.calibrationButtons = {
            "CALI_X1": self.ui.calibrateX1Button,
            "CALI_X2": self.ui.calibrateX2Button,
            "CALI_Y1": self.ui.calibrateY1Button,
            "CALI_Y2": self.ui.calibrateY2Button,
        }

        self.calibrationView = CalibrationView(self.rawLineEdits, self.mapLineEdits)
        self.calibrationData = CalibrationData()
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())

    def uiCalibrationConnects(self):
        """Connect UI elements for data calibration."""
        for label in self.calibrationButtons.keys():
            self.calibrationButtons[label].clicked.connect(
                partial(self.calibrate, label)
            )

        for button in self.pageButtons.values():
            button.clicked.connect(self.turnOffCalibration)

        for lineEdit in (
            list(self.rawLineEdits.values()) 
            + list(self.mapLineEdits.values())
        ):
            lineEdit.editingFinished.connect(self.updateCalibration)

        self.ui.swapXYButton.clicked.connect(self.swapXY)

        self.calibrationData.caliClicked.connect(self.postCalibrationClicked)

    @Slot()
    def turnOffCalibration(self):
        """
        Turn off calibration when the calibration check box is unchecked manually.
        """
        # model off and plot stuff off
        self.calibrationData.calibrationOff()

        # cali view off
        self._resetHighlightButtons()

    @Slot()
    def postCalibrationClicked(self, label: str, data: float):
        self._highlightCaliButton(
            self.calibrationButtons[label], reset=True
        )
        # update the raw line edits by the value of the clicked point
        self.rawLineEdits[label].setText(str(data))
        self.rawLineEdits[label].home(False)
        # highlight the map line edit
        self.mapLineEdits[label].selectAll()
        self.mapLineEdits[label].setFocus()

    def calibrationButtonIsChecked(self):
        """
        Check if any of the calibration buttons is checked
        """
        for label in self.calibrationButtons:
            if self.calibrationButtons[label].isChecked():
                return True
        return False

    def line_select_callback(self, eclick, erelease):
        """
        Callback for line selection.

        *eclick* and *erelease* are the press and release events.
        """
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        # print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")
        # print(f" The buttons you used were: {eclick.button} {erelease.button}")

    def _highlightCaliButton(self, button: QPushButton, reset: bool = False):
        """Highlight the button by changing its color."""
        if reset:
            button.setStyleSheet("")
        else:
            button.setStyleSheet("QPushButton {background-color: #BE82FA}")

    def _resetHighlightButtons(self):
        """Reset the highlighting of all calibration buttons."""
        for label in self.calibrationButtons:
            self._highlightCaliButton(self.calibrationButtons[label], reset=True)

    @Slot()
    def swapXY(self):
        """Swap the x and y axis of the calibration data."""
        rawx1 = self.rawLineEdits["CALI_X1"].value()
        rawx2 = self.rawLineEdits["CALI_X2"].value()
        rawy1 = self.rawLineEdits["CALI_Y1"].value()
        rawy2 = self.rawLineEdits["CALI_Y2"].value()
        mapx1 = self.mapLineEdits["CALI_X1"].value()
        mapx2 = self.mapLineEdits["CALI_X2"].value()
        mapy1 = self.mapLineEdits["CALI_Y1"].value()
        mapy2 = self.mapLineEdits["CALI_Y2"].value()
        self.rawLineEdits["CALI_X1"].setText(str(rawy1))
        self.rawLineEdits["CALI_Y1"].setText(str(rawx1))
        self.rawLineEdits["CALI_X2"].setText(str(rawy2))
        self.rawLineEdits["CALI_Y2"].setText(str(rawx2))
        self.mapLineEdits["CALI_X1"].setText(str(mapy1))
        self.mapLineEdits["CALI_Y1"].setText(str(mapx1))
        self.mapLineEdits["CALI_X2"].setText(str(mapy2))
        self.mapLineEdits["CALI_Y2"].setText(str(mapx2))
        self.updateCalibration()

    @Slot()
    def calibrate(self, calibrationLabel: str):
        """
        Mouse click on one of the calibration buttons prompts switching to
        calibration mode. Mouse cursor crosshair is adjusted and canvas waits for
        click setting calibration point x or y component.
        Besides, the button is highlighted.
        """
        if self.calibrationData.calibrationIsOn == calibrationLabel:
            # already turned on, then turn it off
            self.turnOffCalibration()
            return 

        # button highlighting
        self._resetHighlightButtons()
        self._highlightCaliButton(self.calibrationButtons[calibrationLabel])

        # let the plotting know that calibration is on
        self.calibrationData.calibrationOn(calibrationLabel)

    @Slot()
    def updateCalibration(self):
        """Transfer new calibration data from CalibrationView over to calibrationData
        instance. If the model is currently applying the calibration, then emit
        signal to rewrite the table."""
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())
        if self.calibrationData.applyCalibration:
            self.activeDataset.emitDataSwitched()
    
    # extract and tag ##################################################
    # ##################################################################
    def extractingMVCInits(self, hilbertspace: HilbertSpace):
        """Set up the main class instances holding the data extracted from placing
        markers on the canvas. The AllExtractedData instance holds all data, whereas the
        ActiveExtractedData instance holds data of the currently selected data set."""
        # ui grouping: Labeling
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
        # ui grouping: extracted data management
        self.uiExtractedDataManagements = {
            "new": self.ui.newRowButton,
            "delete": self.ui.deleteRowButton,
            "clear": self.ui.clearAllButton,
        }

        self.activeDataset = ActiveExtractedData()
        self.allDatasets = AllExtractedData()
        self.allDatasets.setCalibrationFunc(self.calibrationData.calibrateDataset)

        self.extractingView = ExtractingView(
            [subsys.id_str for subsys in hilbertspace.subsystem_list],
            (
                self.uiLabelBoxes, self.uiLabelRadioButtons, 
                self.uiBareLabelInputs, self.uiDressedLabelInputs,
                self.uiExtractedDataManagements, 
                self.ui.datasetListView,
                self.ui.bareLabelOrder,
            )
        )

        self.extractingCtrl = ExtractingCtrl(
            (self.allDatasets, self.activeDataset),
            self.extractingView,
        )

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
        self.prefitParamModelConnects()
        self.setUpPrefitRunConnects()

    def prefitStaticElementsBuild(self):
        self.prefitResult = StatusModel()
        # self.spectrumData = CalculatedSpecData()
        self.setUpPrefitResultConnects()
        self.prefitConnects()

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
            # spectrum_data=self.spectrumData,
            calibration_data=self.calibrationData,
            extracted_data=self.allDatasets,
            prefit_result=self.prefitResult,
        )

    @Slot()
    def onPrefitPlotClicked(self):
        """
        Model & View updates
        """
        self.quantumModel.sweep2SpecNMSE(
            slider_or_fit_parameter_set=self.sliderParameterSet,
            sweep_parameter_set=self.sweepParameterSet,
            # spectrum_data=self.spectrumData,
            extracted_data=self.allDatasets,
            calibration_data=self.calibrationData,
            result=self.prefitResult,
        )

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
            self.prefitResult.statusStrForView
        )
        mse_change_ui_setter = lambda: self.ui.mseLabel.setText(
            self.prefitResult.displayed_MSE
        )

        self.prefitResult.setupUISetters(
            status_type_ui_setter=status_type_ui_setter,
            status_text_ui_setter=status_text_ui_setter,
            mseChangeUISetter=mse_change_ui_setter,
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

    def prefitConnects(self):
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

        # connect the run button callback to the generation and run of parameter sweep
        # notice that parameter update is done in the slider connects
        # TODO: here is a bug, since the parameter update is done in the slider connects,
        # if parameters are updated due to the fitting step, and the fitting result parameters
        # are not imported to the prefit parameters, then the HilbertSpace is still using the
        # fit parameters; if user want to plot with prefit parameters, clicking the plot button
        # in the prefit will not update the parameters based on the sliders.
        self.ui.plotButton.clicked.connect(self.onPrefitPlotClicked)

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

        self.fitResult = StatusModel()
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
        self.dataExportButtons["fit"].clicked.connect(
            lambda: self.sliderParameterSet.update(self.fitParameterSet)
        )
        self.dataExportButtons["prefit"].clicked.connect(
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
            self.fitResult.statusStrForView
        )
        mse_change_ui_setter = lambda: self.ui.mseLabel_2.setText(
            self.fitResult.displayed_MSE
        )

        self.fitResult.setupUISetters(
            status_type_ui_setter=status_type_ui_setter,
            status_text_ui_setter=status_text_ui_setter,
            mseChangeUISetter=mse_change_ui_setter,
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

        self.extractingCtrl.dynamicalInit()
        self.prefitDynamicalElementsBuild(hilbertspace)
        self.fitDynamicalElementsBuild()

        self.plottingCtrl.dynamicalInit(
            self.measurementData, self.quantumModel
        )

        self.allDatasets.loadedFromRegistry.connect(self.extractedDataSetup)

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
        self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())

        # set dataset
        self.allDatasets.layoutChanged.emit()  # update the list view to show the new data
        self.allDatasets.emitFocusChanged()
        self.allDatasets.emitXUpdated()

    def resizeAndCenter(self, maxSize: QSize):
        newSize = QSize(maxSize.width() * 0.9, maxSize.height() * 0.9)
        maxRect = QRect(QPoint(0, 0), maxSize)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, newSize, maxRect)
        )

    # error message system #############################################
    # ##################################################################
    def statusMVCInits(self):
        self.status = StatusModel()
        self.statusBarView = StatusBarView(self.ui.statusBar)
        self.statusCtrl = StatusCtrl(
            (self.allDatasets, self.activeDataset), 
            self.status, 
            self.statusBarView,
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
