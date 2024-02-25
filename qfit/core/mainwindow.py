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
    SignalInstance,
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

from qfit.utils.helpers import executed_in_ipython
from qfit.models.measurement_data import MeasurementDataType, MeasDataSet
from qfit.controllers.help_tooltip import HelpButtonCtrl
from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

# settings
from qfit.controllers.settings import SettingsCtrl
from qfit.widgets.settings import (
    VisualSettingsWidget,
    FitSettingsWidget,
    NumericalSpectrumSettingsWidget,
    SettingsWidgetSet,
)
from qfit.ui_designer.settings_fit import Ui_fitSettingsWidget
from qfit.ui_designer.settings_numerical_spectrum import (
    Ui_numericalSpectrumSettingsWidget,
)
from qfit.ui_designer.settings_visual import Ui_visualSettingsWidget

# paging:
from qfit.views.paging import PageView

# calibration:
# from qfit.models.calibration_data import CalibrationData
from qfit.models.quantum_model_parameters import CaliParamModel
from qfit.views.calibration import CalibrationView
from qfit.controllers.calibration import CalibrationCtrl

# extract
from qfit.models.extracted_data import ActiveExtractedData, AllExtractedData
from qfit.controllers.extracting import ExtractingCtrl
from qfit.views.extracting import ExtractingView

# status bar
from qfit.models.status import StatusModel
from qfit.controllers.status import StatusCtrl
from qfit.views.status_bar import StatusBarView

# pre-fit
from qfit.views.parameters import PrefitParamView
from qfit.views.prefit import PrefitView
from qfit.models.data_structures import QMSliderParam, QMSweepParam
from qfit.models.quantum_model_parameters import (
    ParamSet,
    HSParamSet,
)
from qfit.models.prefit import PrefitParamModel, PrefitCaliModel
from qfit.models.numerical_model import QuantumModel

# fit
from qfit.models.data_structures import QMFitParam
from qfit.views.parameters import FitParamView
from qfit.models.fit import FitParamModel, FitModel

# plot
from qfit.controllers.plotting import PlottingCtrl

# registry
from qfit.models.registry import Registry, RegistryEntry, Registrable

# menu controller
from qfit.controllers.io_menu import IOCtrl

if TYPE_CHECKING:
    from qfit.models.parameter_settings import ParameterType


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

    def __init__(self):
        QMainWindow.__init__(self)
        self.openFromIPython = executed_in_ipython()
        self.setFocusPolicy(Qt.StrongFocus)

        self.measurementData = MeasDataSet([])

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setShadows()
        self.ui.verticalSnapButton.setAutoExclusive(False)

        # navigation
        self.ui_menu = MenuWidget(parent=self)
        self.pagingMVCInits()

        # settings
        self.ui_settings = SettingsWidgetSet(
            visual=VisualSettingsWidget(self),
            fit=FitSettingsWidget(self),
            numericalSpectrum=NumericalSpectrumSettingsWidget(self),
        )
        self.settingsMVCInit()

        # calibration - should be inited after prefit, as it requires a sweep parameter set
        self.calibrationMVCInits()

        # extract
        self.extractingMVCInits()

        # prefit: controller, two models and their connection to view (sliders)
        self.prefitMVCInits()

        # fit
        self.fitMVCInits()

        # plot, mpl canvas
        self.plottingMVCInits()

        # help button
        self.helpButtonMVCInits()

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

    def initializeDynamicalElements(
        self,
        hilbertspace: HilbertSpace,
        measurementData: List[MeasurementDataType],
    ):
        self.calibrationCtrl.dynamicalInit(hilbertspace, measurementData)
        self.extractingCtrl.dynamicalInit(hilbertspace, measurementData)
        self.prefitDynamicalElementsBuild(hilbertspace, measurementData)
        self.fitDynamicalElementsBuild(hilbertspace)
        self.plottingCtrl.dynamicalInit(measurementData)

        self.register()

        self.raise_()

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

    # settings #########################################################
    ####################################################################
    def settingsMVCInit(self):
        self.settingsButtonSet = {
            "visual": self.ui.extractSettingsPushButton,
            "fit": self.ui.fitSettingsPushButton,
            "numericalSpectrum": self.ui.prefitSettingsPushButton,
        }
        self.settingsCtrl = SettingsCtrl(self.ui_settings, self.settingsButtonSet)

    # help button and gif tooltip ######################################
    ####################################################################
    def helpButtonMVCInits(self):
        self.helpButtons = {
            "calibration": self.ui.calibrationHelpPushButton,
            "fit": self.ui.fitHelpPushButton,
            "fitResult": self.ui_settings.fit.ui.fitResultHelpPushButton,
            "prefitResult": self.ui_settings.numericalSpectrum.ui.prefitResultHelpPushButton,
            "numericalSpectrumSettings": self.ui_settings.numericalSpectrum.ui.numericalSpectrumSettingsHelpPushButton,
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
            "topHat": self.ui_settings.visual.ui.topHatCheckBox,
            "wavelet": self.ui_settings.visual.ui.waveletCheckBox,
            "edge": self.ui_settings.visual.ui.edgeFilterCheckBox,
            "bgndX": self.ui_settings.visual.ui.bgndSubtractXCheckBox,
            "bgndY": self.ui_settings.visual.ui.bgndSubtractYCheckBox,
            "log": self.ui_settings.visual.ui.logScaleCheckBox,
            "min": self.ui_settings.visual.ui.rangeSliderMin,
            "max": self.ui_settings.visual.ui.rangeSliderMax,
            "color": self.ui_settings.visual.ui.colorComboBox,
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
                self.measurementData,
                self.caliParamModel,
                self.allDatasets,
                self.activeDataset,
                self.quantumModel,
            ),
            (
                self.measComboBoxes,
                self.measPlotSettings,
                self.ui.swapXYButton,
                self.canvasTools,
                self.calibrationButtons,
                self.ui.calibratedCheckBox,
                self.pageView,
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
            "fit": self.ui.exportToPrefitButton,
            "prefit": self.ui.exportToFitButton,
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
            "X0": self.ui.rawX1LineEdit,
            "X1": self.ui.rawX2LineEdit,
            "Y0": self.ui.rawY1LineEdit,
            "Y1": self.ui.rawY2LineEdit,
        }
        self.mapLineEdits = {
            "X0": self.ui.mapX1LineEdit,
            "X1": self.ui.mapX2LineEdit,
            "Y0": self.ui.mapY1LineEdit,
            "Y1": self.ui.mapY2LineEdit,
        }
        self.calibrationButtons = {
            "X0": self.ui.calibrateX1Button,
            "X1": self.ui.calibrateX2Button,
            "Y0": self.ui.calibrateY1Button,
            "Y1": self.ui.calibrateY2Button,
        }

        self.caliParamModel = CaliParamModel()
        self.calibrationView = CalibrationView(
            rawLineEdits=self.rawLineEdits,
            mapLineEdits=self.mapLineEdits,
            calibrationButtons=self.calibrationButtons,
        )

        self.calibrationCtrl = CalibrationCtrl(
            self.caliParamModel, self.calibrationView, self.pageButtons
        )
        # self.calibrationData = CalibrationData()
        # self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())

    # def _highlightCaliButton(self, button: QPushButton, reset: bool = False):
    #     """
    #     SHOULD GO TO CALIBRATION VIEW
    #     Highlight the button by changing its color."""
    #     if reset:
    #         button.setStyleSheet("")
    #     else:
    #         button.setStyleSheet("QPushButton {background-color: #BE82FA}")

    # def _resetHighlightButtons(self):
    #     """Reset the highlighting of all calibration buttons."""
    #     for label in self.calibrationButtons:
    #         self._highlightCaliButton(self.calibrationButtons[label], reset=True)

    # extract and tag ##################################################
    # ##################################################################
    def extractingMVCInits(self):
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
        # self.allDatasets.setCalibrationFunc(self.calibrationData.calibrateDataset)

        self.extractingView = ExtractingView(
            (
                self.uiLabelBoxes,
                self.uiLabelRadioButtons,
                self.uiBareLabelInputs,
                self.uiDressedLabelInputs,
                self.uiExtractedDataManagements,
                self.ui.datasetListView,
                self.ui.bareLabelOrder,
            ),
        )

        self.extractingCtrl = ExtractingCtrl(
            (self.allDatasets, self.activeDataset),
            self.extractingView,
        )

    # Pre-fit ##########################################################
    # ##################################################################
    def prefitMVCInits(self):
        # UI grouping
        self.prefitOptions = {
            "subsysToPlot": self.ui_settings.numericalSpectrum.ui.subsysComboBox,
            "initialState": self.ui_settings.numericalSpectrum.ui.initStateLineEdit,
            "photons": self.ui_settings.numericalSpectrum.ui.prefitPhotonSpinBox,
            "evalsCount": self.ui_settings.numericalSpectrum.ui.evalsCountLineEdit,
            "pointsAdded": self.ui_settings.numericalSpectrum.ui.pointsAddLineEdit,
            "autoRun": self.ui.autoRunCheckBox,
        }

        self.quantumModel = QuantumModel()

        self.prefitParamModel = PrefitParamModel()
        self.prefitCaliModel = PrefitCaliModel()
        self.prefitParamView = PrefitParamView(
            self.ui.prefitScrollAreaWidget,
            self.ui.prefitMinmaxScrollAreaWidget,
        )
        self.prefitView = PrefitView(
            runSweep=self.ui.plotButton,
            options=self.prefitOptions,
        )

        self.prefitResult = StatusModel()
        self.prefitStaticElementsBuild()

    def prefitStaticElementsBuild(self):
        self.quantumModelConnects()
        self.prefitButtonConnects()
        self.prefitSliderParamConnects()
        self.prefitCaliConnects()

    def prefitDynamicalElementsBuild(
        self, hilbertspace: HilbertSpace, measurementData: List[MeasurementDataType]
    ):
        self.prefitBuildParamSet(hilbertspace)
        self.prefitViewInsertParams()
        self.prefitView.dynamicalInit(
            subsysNames=[
                HSParamSet.parentSystemNames(subsys)
                for subsys in hilbertspace.subsystem_list[::-1]
            ],
            hilbertDim=hilbertspace.dimension,
        )
        self.quantumModel.dynamicalInit(
            hilbertspace, [data.name for data in measurementData]
        )

        # update everything in the view
        self.prefitParamModel.emitUpdateBox()
        self.prefitParamModel.emitUpdateSlider()
        self.prefitCaliModel.emitUpdateBox()
        self.prefitCaliModel.emitUpdateSlider()

        # update everything in the quantumModel
        self.quantumModel.disableSweep = True  # disable the auto sweep
        self.prefitParamModel.emitHSUpdated()
        self.allDatasets.emitDataUpdated()
        self.caliParamModel.sendXCaliFunc()
        self.caliParamModel.sendYCaliFunc()
        self.prefitView.emitAllOptions()  # auto run sync to the view
        # self.quantumModel.disableSweep = False

    def prefitBuildParamSet(self, hilbertspace: HilbertSpace):
        """
        Should belong to PREFIT PARAMETER CONTROLLER

        identify prefit slider parameters
        """

        # check how many sweep parameters are found and create sliders
        # for the remaining parameters
        sweepParameterSet = HSParamSet.sweepSetByHS(hilbertspace)
        param_types: set["ParameterType"] = set(
            sweepParameterSet.getAttrDict("paramType").values()
        )

        if len(sweepParameterSet) == 0:
            print(
                "No sweep parameter (ng / flux) is found in the HilbertSpace "
                "object. Please check your quantum model."
            )
            self.close()

        elif len(sweepParameterSet) == 1:
            # only one sweep parameter is found, so we can create sliders
            # for the remaining parameters
            excluded: List[ParameterType] = ["cutoff", "truncated_dim", "l_osc"]
            self.prefitParamModel.dynamicalInit(
                hilbertspace=hilbertspace,
                excluded_parameter_type=(
                    excluded + [list(param_types)[0]]  # exclude the sweep parameter
                ),
            )

        elif len(sweepParameterSet) == 2 and param_types == set(["flux", "ng"]):
            # a flux and ng are detected in the HilbertSpace object
            # right now, we assume that the flux is always swept in this case
            self.prefitParamModel.dynamicalInit(
                hilbertspace=hilbertspace,
                excluded_parameter_type=["flux", "cutoff", "truncated_dim", "l_osc"],
            )

        else:
            print(
                "Unfortunately, the current version of qfit does not support "
                "multiple sweep parameters (flux / ng). This feature will be "
                "available in the next release."
            )
            self.close()

        # initialize calibration sliders
        self.prefitCaliModel.setAttrByParamDict(
            self.caliParamModel.toPrefitParams(),
            insertMissing=True,
        )

    def prefitViewInsertParams(self):
        """
        THIS METHOS BELONGS TO THE PREFIT PARAMETER CONTROLLER

        Notably, this function do not need to be regenerated when reloaded,
        as it only connect the view with the model, which will not be changed.

        (only the elements in the view will be changed, but the view itself
        will not be changed)
        """
        # initialize the sliders, boxes and minmax
        HSParamNames = self.prefitParamModel.paramNamesDict()
        caliParamNames = self.prefitCaliModel.paramNamesDict()
        self.prefitParamView.insertSliderMinMax(
            HSParamNames, caliParamNames, removeExisting=True
        )

    def prefitSliderParamConnects(self):
        """
        View --> model: slider --> parameter

        Note that in the current implementation, main window is both the
        controller and the model (hosting the parameterset)
        """
        # update the value
        for signalSet, model in [
            (self.prefitParamView.HSSignals, self.prefitParamModel),
            (self.prefitParamView.caliSignals, self.prefitCaliModel),
        ]:
            signalSet: Dict[str, SignalInstance]
            model: Union[PrefitParamModel, PrefitCaliModel]

            signalSet["sliderChanged"].connect(
                lambda paramAttr, model=model: model.storeParamAttr(
                    paramAttr, fromSlider=True
                )
            )
            signalSet["textChanged"].connect(
                lambda paramAttr, model=model: model.storeParamAttr(paramAttr)
            )
            signalSet["rangeEditingFinished"].connect(
                lambda paramAttr, model=model: model.storeParamAttr(paramAttr)
            )

            # synchronize slider and box
            model.updateSlider.connect(
                lambda paramAttr: self.prefitParamView.setByParamAttr(
                    paramAttr, toSlider=True
                )
            )
            model.updateBox.connect(
                lambda paramAttr: self.prefitParamView.setByParamAttr(
                    paramAttr, toSlider=False
                )
            )

            # self.prefitParamView.HSSliderChanged.connect(
            #     lambda paramAttr: self.prefitParamModel.storeParamAttr(
            #         paramAttr, fromSlider=True
            #     )
            # )
            # self.prefitParamView.HSTextChanged.connect(
            #     lambda paramAttr: self.prefitParamModel.storeParamAttr(paramAttr)
            # )
            # self.prefitParamView.HSRangeEditingFinished.connect(
            #     lambda paramAttr: self.prefitParamModel.storeParamAttr(paramAttr)
            # )
            # self.prefitParamView.HSEditingFihished.connect(
            #     self.prefitParamModel.updateParent
            # )

            # # synchronize slider and box
            # self.prefitParamModel.updateSlider.connect(
            #     lambda paramAttr: self.prefitParamView.setByParamAttr(
            #         paramAttr, toSlider=True
            #     )
            # )
            # self.prefitParamModel.updateBox.connect(
            #     lambda paramAttr: self.prefitParamView.setByParamAttr(
            #         paramAttr, toSlider=False
            #     )
            # )

        # update hilbert space
        self.prefitParamView.HSEditingFinished.connect(
            self.prefitParamModel.updateParent
        )
        # update cali model
        self.prefitParamView.caliEditingFinished.connect(
            self.prefitCaliModel.emitUpdateCaliModel
        )

    def prefitCaliConnects(self):
        self.prefitCaliModel.updateCaliModel.connect(self.caliParamModel.setParamByPA)
        self.caliParamModel.updatePrefitModel.connect(self.prefitCaliModel.setParamByPA)

    def quantumModelConnects(self):
        self.prefitParamModel.hilbertSpaceUpdated.connect(
            self.quantumModel.updateHilbertSpace
        )
        self.allDatasets.dataUpdated.connect(self.quantumModel.updateExtractedData)
        self.caliParamModel.xCaliUpdated.connect(self.quantumModel.updateSweepParamSets)
        self.caliParamModel.yCaliUpdated.connect(self.quantumModel.updateYCaliFunc)
        self.caliParamModel.invYCaliUpdated.connect(
            self.quantumModel.updateInvYCaliFunc
        )

        # connect the page change to the disable sweep
        self.pageView.pageChanged.connect(
            self.quantumModel.updateDisableSweepOnPageChange
        )

    def prefitButtonConnects(self):
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

        self.prefitView.optionUpdated.connect(self.quantumModel.updateSweepOption)

        self.prefitView.runSweep.clicked.connect(self.quantumModel.sweep2SpecMSE)

    # Fit ##############################################################
    # ##################################################################
    def fitMVCInits(self):
        self.fitParamView = FitParamView(
            self.ui.fitScrollAreaWidget,
        )
        self.fitParamModel = FitParamModel()
        self.fitModel = FitModel()

        self.fitStaticElementsBuild()

    def fitDynamicalElementsBuild(self, hilbertspace: HilbertSpace):
        self.fitParamModel.dynamicalInit(
            hilbertspace=hilbertspace,
            excluded_parameter_type=["ng", "flux", "cutoff", "truncated_dim", "l_osc"],
        )
        self.fitParamView.fitTableInserts(
            self.fitParamModel.paramNamesDict(), removeExisting=True
        )

    def fitStaticElementsBuild(self):
        self.fitOptionConnects()
        self.fitTableParamConnects()
        self.fitPushButtonConnects()

    @Slot()
    def fittingParameterLoad(self, source: Literal["prefit", "fit"]):
        """
        Load the initial value, min, and max from the source parameter set
        """
        if source == "prefit":
            init_value_dict = self.prefitParamModel.getAttrDict("value")
        elif source == "fit":
            init_value_dict = self.fitParamModel.getAttrDict("value")

        self.fitParamModel.setAttrByAttrDict(init_value_dict, "initValue")
        self.fitParamModel.setAttrByAttrDict(init_value_dict, "value")
        max_value_dict = {
            key: (value * 1.2 if value > 0 else value * 0.8)
            for key, value in init_value_dict.items()
        }
        self.fitParamModel.setAttrByAttrDict(max_value_dict, "max")
        min_value_dict = {
            key: (value * 0.8 if value > 0 else value * 1.2)
            for key, value in init_value_dict.items()
        }
        self.fitParamModel.setAttrByAttrDict(min_value_dict, "min")

    @Slot()
    def prefitParamLoad(self):
        value_dict = self.fitParamModel.getAttrDict("value")
        self.prefitParamModel.setAttrByAttrDict(value_dict, "value")

    def _costFunction(self, paramDict: Dict[str, float]) -> float:
        """
        Cook up a cost function for the optimization
        """
        self.fitParamModel.setAttrByAttrDict(paramDict, "value")
        for params in self.fitParamModel.values():
            for p in params.values():
                p.setParameterForParent()

        self.quantumModel.updateHSWoCalc(self.fitParamModel.hilbertspace)

        return self.quantumModel.updateCalc()

    @Slot()
    def optimizeParams(self):
        if not self.fitParamModel.isValid:
            return

        # configure other models & views
        self.quantumModel.sweepUsage = "fit"
        self.ui.fitButton.setEnabled(False)
        self.prefitParamView.sliderSet.setEnabled(False)

        # setup the optimization
        self.fitModel.setupOptimization(
            fixedParams=self.fitParamModel.fixedParams,
            freeParamRanges=self.fitParamModel.freeParamRanges,
            costFunction=self._costFunction,
        )

        # cook up a cost function
        self.fitModel.runOptimization(
            initParam=self.fitParamModel.initParams,
        )

    @Slot()
    def postOptimization(self):
        self.ui.fitButton.setEnabled(True)
        self.prefitParamView.sliderSet.setEnabled(True)
        self.quantumModel.sweepUsage = "prefit"

    def fitOptionConnects(self):
        self.ui_settings.fit.ui.tolLineEdit.editingFinished.connect(
            lambda: self.fitParamModel.updateTol(
                self.ui_settings.fit.ui.tolLineEdit.value()
            )
        )
        self.ui_settings.fit.ui.optimizerComboBox.currentIndexChanged.connect(
            lambda: self.fitParamModel.updateOptimizer(
                self.ui_settings.fit.ui.optimizerComboBox.currentText()
            )
        )

    def fitPushButtonConnects(self):
        """
        Connect the buttons for
        1. run fit
        2. parameters transfer: prefit to fit
        3. parameters transfer: fit to prefit
        4. parameters transfer: fit result to fit
        """
        # run optimization
        self.ui.fitButton.clicked.connect(self.optimizeParams)

        # the prefit parameter export to fit
        self.dataExportButtons["prefit"].clicked.connect(
            lambda: self.fitParamModel.setAttrByParamDict(
                self.prefitParamModel.toFitParams(),
                attrsToUpdate=["value", "min", "max", "initValue"],
                insertMissing=False,
            )
        )
        # the fit parameter export to prefit
        self.dataExportButtons["fit"].clicked.connect(
            lambda: self.prefitParamModel.setAttrByParamDict(
                self.fitParamModel.toPrefitParams(),
                attrsToUpdate=["value"],
                insertMissing=False,
            )
        )
        # the final value to initial value
        self.ui.pushButton_2.clicked.connect(
            lambda: self.fitParamModel.setAttrByParamDict(
                self.fitParamModel.toInitParams(),
                attrsToUpdate=["initValue"],
                insertMissing=False,
            )
        )

    def fitTableParamConnects(self):
        """
        table --> parameter

        Note that in the current implementation, main window is both the
        controller and the model (hosting the parameterset)
        """
        # update the value
        self.fitParamView.dataEditingFinished.connect(
            self.fitParamModel._storeParamAttr
        )
        self.fitParamModel.updateBox.connect(self.fitParamView.setBoxValue)

    def fitConnects(self):
        self.fitModel.optFinished.connect(self.postOptimization)

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
        self.registry.register(self.caliParamModel)
        self.registry.register(self.allDatasets)

        # parameters
        self.registry.register(self.prefitParamModel)
        self.registry.register(self.fitParamModel)

        # main window
        self.registry.register(self)

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
