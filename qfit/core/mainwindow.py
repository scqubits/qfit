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
)
from PySide6.QtGui import QColor, QMouseEvent, Qt
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QMainWindow,
    QStyle,
)

from qfit.utils.helpers import executed_in_ipython
from qfit.models.measurement_data import MeasurementDataType, MeasDataSet
from qfit.controllers.help_tooltip import HelpButtonCtrl
from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

# settings
from qfit.controllers.settings import SettingsCtrl
from qfit.widgets.settings import (
    SettingsWidget,
)

# paging:
from qfit.views.paging_view import PageView

# calibration:
from qfit.models.calibration import CaliParamModel
from qfit.views.calibration_view import CalibrationView
from qfit.controllers.calibration_ctrl import CalibrationCtrl

# extract
from qfit.models.extracted_data import ActiveExtractedData, AllExtractedData
from qfit.controllers.extracting_ctrl import ExtractingCtrl
from qfit.views.extracting_view import ExtractingView

# status bar
from qfit.models.status import StatusModel
from qfit.controllers.status import StatusCtrl
from qfit.views.status_bar import StatusBarView

# pre-fit
from qfit.views.prefit_view import PrefitParamView, PrefitView
from qfit.models.prefit import PrefitParamModel, PrefitCaliModel
from qfit.models.numerical_model import QuantumModel
from qfit.controllers.prefit_ctrl import PrefitCtrl

# fit
from qfit.views.fit_view import FitParamView, FitView
from qfit.models.fit import FitParamModel, FitCaliModel, FitModel
from qfit.controllers.fit_ctrl import FitCtrl

# plot
from qfit.controllers.plotting_ctrl import PlottingCtrl

# registry
from qfit.models.registry import Registry, RegistryEntry, Registrable

# menu controller
from qfit.controllers.io_menu_ctrl import IOCtrl


mpl.rcParams["toolbar"] = "None"


# metaclass: solve the incompatibility and make the mainWindow registrable
class CombinedMeta(type(QMainWindow), type(Registrable)):
    pass


class MainWindow(QMainWindow, Registrable, metaclass=CombinedMeta):
    """Class for the main window of the app."""

    statusModel: StatusModel

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
        self.ui.verticalSnapButton.setAutoExclusive(False)

        # navigation
        self.ui_menu = MenuWidget(parent=self)
        self.pagingMVCInits()

        # settings
        self.ui_settings = SettingsWidget(self)
        self.settingsMVCInit()

        # set shadows
        self.setShadows()

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
        self.prefitCtrl.dynamicalInit(hilbertspace, measurementData)
        self.fitCtrl.dynamicalInit()
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

        for widget in [self.ui_settings]:
            eff = QGraphicsDropShadowEffect(widget)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            widget.setGraphicsEffect(eff)

    # settings #########################################################
    ####################################################################
    def settingsMVCInit(self):
        self.settingsCtrl = SettingsCtrl(self.ui_settings, self.ui.settingsPushButton)

    # help button and gif tooltip ######################################
    ####################################################################
    def helpButtonMVCInits(self):
        self.helpButtons = {
            "calibration": self.ui.calibrationHelpPushButton,
            "fit": self.ui.fitHelpPushButton,
            "numericalSpectrumSettings": self.ui_settings.ui.numericalSpectrumSettingsHelpPushButton,
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
            "topHat": self.ui_settings.ui.topHatCheckBox,
            "wavelet": self.ui_settings.ui.waveletCheckBox,
            "edge": self.ui_settings.ui.edgeFilterCheckBox,
            "bgndX": self.ui_settings.ui.bgndSubtractXCheckBox,
            "bgndY": self.ui_settings.ui.bgndSubtractYCheckBox,
            "log": self.ui_settings.ui.logScaleCheckBox,
            "min": self.ui_settings.ui.rangeSliderMin,
            "max": self.ui_settings.ui.rangeSliderMax,
            "color": self.ui_settings.ui.colorComboBox,
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
        self.dataTransferButtons = {
            "fit": self.ui.exportToPrefitButton,
            "prefit": self.ui.exportToFitButton,
            "init": self.ui.pushButton_2,
        }
        self.pageStackedWidgets = {
            "center": self.ui.pagesStackedWidget,
            # "bottom": self.ui.bottomStackedWidget,
        }

        self.pageView = PageView(
            self.pageButtons, self.dataTransferButtons, self.pageStackedWidgets
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
            "subsysToPlot": self.ui_settings.ui.subsysComboBox,
            "initialState": self.ui_settings.ui.initStateLineEdit,
            "photons": self.ui_settings.ui.prefitPhotonSpinBox,
            "evalsCount": self.ui_settings.ui.evalsCountLineEdit,
            "pointsAdded": self.ui_settings.ui.pointsAddLineEdit,
            "autoRun": self.ui.autoRunCheckBox,
        }

        self.quantumModel = QuantumModel()

        self.prefitParamModel = PrefitParamModel()
        self.prefitCaliModel = PrefitCaliModel()
        self.prefitParamView = PrefitParamView(
            self.ui.prefitScrollAreaWidget,
            self.ui.prefitMinmaxScrollAreaWidget,
            self.ui.frame_prefit_minmax,
        )
        self.prefitView = PrefitView(
            runSweep=self.ui.plotButton,
            options=self.prefitOptions,
        )

        self.prefitCtrl = PrefitCtrl(
            (
                self.quantumModel, self.prefitParamModel, self.prefitCaliModel,
                self.allDatasets, self.caliParamModel, 
                self.measurementData, self
            ),
            (self.prefitView, self.prefitParamView, self.pageView),
        )


    # Fit ##############################################################
    # ##################################################################
    def fitMVCInits(self):
        # ui grouping
        self.fitOptions = {
            "tol": self.ui_settings.ui.tolLineEdit,
            "optimizer": self.ui_settings.ui.optimizerComboBox,
        }


        self.fitParamView = FitParamView(
            self.ui.fitScrollAreaWidget,
        )
        self.fitView = FitView(
            self.ui.fitButton,
            self.dataTransferButtons,
            self.fitOptions,
        )
        self.fitParamModel = FitParamModel()
        self.fitCaliModel = FitCaliModel()
        self.fitModel = FitModel()

        self.fitCtrl = FitCtrl(
            (
                self.fitModel, self.fitParamModel, self.fitCaliModel,
                self.prefitParamModel, self.prefitCaliModel, self.quantumModel,
                self.allDatasets, self.caliParamModel,
                self.measurementData
            ),
            (self.fitView, self.fitParamView, self.prefitParamView),
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
        self.registry.register(self.caliParamModel)
        self.registry.register(self.allDatasets)

        # parameters
        self.registry.register(self.prefitParamModel)
        self.registry.register(self.fitParamModel)
        self.registry.register(self.prefitCaliModel)
        self.registry.register(self.fitCaliModel)

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
        self.statusModel = StatusModel()
        self.statusBarView = StatusBarView(self.ui.statusBar)
        self.statusCtrl = StatusCtrl(
            (
                self.quantumModel, self.fitModel, 
                self.fitParamModel, self.fitCaliModel
            ),
            self.statusModel,
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
