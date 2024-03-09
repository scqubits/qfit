import sys
import os
from copy import deepcopy as _deepcopy
from typing import Union, Dict, Any, Dict, List

from PySide6.QtWidgets import QApplication

from scqubits.core.hilbert_space import HilbertSpace
from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
)

from qfit.core.mainwindow import MainWindow
from qfit.utils.helpers import executed_in_ipython

from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

# help button
from qfit.controllers.help_tooltip import HelpButtonCtrl

# settings
from qfit.controllers.settings import SettingsCtrl
from qfit.widgets.settings import SettingsWidget

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
from qfit.models.prefit import PrefitHSParams, PrefitCaliParams
from qfit.models.numerical_model import QuantumModel
from qfit.controllers.prefit_ctrl import PrefitCtrl

# fit
from qfit.views.fit_view import FitParamView, FitView
from qfit.models.fit import FitHSParams, FitCaliParams, FitModel
from qfit.controllers.fit_ctrl import FitCtrl

# plot
from qfit.controllers.plotting_ctrl import PlottingCtrl

# registry
from qfit.models.registry import Registry

# menu controller
from qfit.controllers.io_ctrl import IOCtrl

# measurement data
from qfit.models.measurement_data import MeasurementDataType, MeasDataSet

import qfit.settings as settings
if executed_in_ipython():
    # inside ipython, the function get_ipython is always in globals()
    ipython = get_ipython()
    ipython.run_line_magic("gui", "qt6")
    settings.EXECUTED_IN_IPYTHON = True
else:
    settings.EXECUTED_IN_IPYTHON = False


class Fit:
    app: Union[QApplication, None] = None
    _mainWindow: MainWindow

    # IOs ####################################################################
    def __new__(cls, *args, **kwargs) -> "Fit":
        # Create a new instance
        instance = object.__new__(cls)

        # Create a new QApplication if it does not exist
        if not settings.EXECUTED_IN_IPYTHON:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            instance.app = app
        else:
            pass

        # main window
        instance._mainWindow = MainWindow()
        instance._MVCInit()
        instance._mainWindow.show()

        return instance

    def __init__(
        self, hilbertSpace: HilbertSpace, measurementFileName: Union[str, None] = None
    ):
        self._mainWindow: MainWindow
            
        self._ioCtrl.newProject(
            from_menu=False, 
            hilbertSpace=hilbertSpace,
            measurementFileName=measurementFileName
        )

        if not settings.EXECUTED_IN_IPYTHON:
            self.app.exec_()

    # methods to create a new project #########################################
    @classmethod
    def new(
        cls,
        hilbertSpace: HilbertSpace,
        measurementFileName: Union[str, None] = None,
    ) -> "Fit":
        """
        Create a qfit project with a `HilbertSpace object` from `scqubits` and
        a measurement file.

        Parameters
        ----------
        hilbertSpace: HilbertSpace
            HilbertSpace object from scqubits
        measurementFileName: str
            Name of measurement file to be loaded. If left blank, a window
            will pop up to ask for a file.

        Returns
        -------
        qfit project
        """
        instance = cls.__new__(cls)
        instance.__init__(hilbertSpace, measurementFileName)

        return instance

    @classmethod
    def open(
        cls,
        fileName: Union[str, None] = None,
    ) -> "Fit":
        """
        Open a qfit project from a file.

        Parameters
        ----------
        fileName: str
            Name of file to be opened.

        Returns
        -------
        qfit project
        """

        instance = cls.__new__(cls)

        # load registry
        instance._ioCtrl.openFile(
            from_menu=False,
            fileName=fileName,
        )

        if not settings.EXECUTED_IN_IPYTHON:
            instance.app.exec_()

        return instance

    # methods to export data ##################################################
    def exportParameters(self, fromFit: bool = True) -> Dict[str, Any]:
        """
        Export the fit parameters to a file. 

        Parameters
        ----------
        fromFit: bool
            As we have two copies of parameters, one from prefit sliders and one from fit tables, please specify which one to export.
        """
        if fromFit:
            return (
                self._fitHSParams.getFlattenedAttrDict("value") 
                | self._fitCaliParams.getFlattenedAttrDict("value")
            )
        else:
            return (
                self._prefitHSParams.getFlattenedAttrDict("value") 
                | self._prefitCaliParams.getFlattenedAttrDict("value")
            )
        
    def exportHilbertSpace(
        self, 
        deepcopy: bool = False,
        fromFit: bool = True
    ) -> HilbertSpace:
        """
        Export the HilbertSpace object.

        Parameters
        ----------
        deepcope: bool
            If True, a deepcopy of the HilbertSpace object is returned.
            If False, the original HilbertSpace object is returned.
        fromFit: bool
            As we have two copies of parameters, one from prefit sliders and one from fit tables, please specify which one to export.
        """

        if fromFit:
            self._fitHSParams.blockSignals(True)
            self._fitHSParams.updateParamForHS()
            self._fitHSParams.blockSignals(False)

            hilbertSpace = self._fitHSParams.hilbertspace

        else:
            self._prefitHSParams.blockSignals(True)
            self._prefitHSParams.updateParamForHS()
            self._prefitHSParams.blockSignals(False)

            hilbertSpace = self._prefitHSParams.hilbertspace

        return _deepcopy(hilbertSpace) if deepcopy else hilbertSpace
    
    # models, views and controllers ####################################
    # ##################################################################
    def _MVCInit(self):
        self._measurementData = MeasDataSet([])

        # main ui
        self._mainUi = Ui_MainWindow()
        self._mainUi.setupUi(self._mainWindow)
        self._mainUi.verticalSnapButton.setAutoExclusive(False)

        # navigation
        self._pagingMVCInits()

        # settings
        self._settingsMVCInit()

        # help button
        self._helpButtonMVCInits()

        # calibration - should be inited after prefit, as it requires a sweep parameter set
        self._calibrationMVCInits()

        # extract
        self._extractingMVCInits()

        # prefit: controller, two models and their connection to view (sliders)
        self._prefitMVCInits()

        # fit
        self._fitMVCInits()

        # plot, mpl canvas
        self._plottingMVCInits()

        # IO
        self._IOMVCInits()

        # status bar
        self._statusMVCInits()

        # set shadows for all buttons
        self._setShadows()

    def _dynamicalInit(
        self,
        hilbertspace: HilbertSpace,
        measurementData: List[MeasurementDataType],
    ):
        self._calibrationCtrl.dynamicalInit(hilbertspace, measurementData)
        self._extractingCtrl.dynamicalInit(hilbertspace, measurementData)
        self._prefitCtrl.dynamicalInit(hilbertspace, measurementData)
        self._fitCtrl.dynamicalInit(hilbertspace)
        self._plottingCtrl.dynamicalInit(measurementData)
        self._ioCtrl.dynamicalInit(hilbertspace)
        self._register()

        self._mainWindow.raise_()

    # ui setup #########################################################
    def _setShadows(self):
        for button in [
            self._mainUi.newRowButton,
            self._mainUi.deleteRowButton,
            self._mainUi.clearAllButton,
            self._mainUi.horizontalSnapButton,
            self._mainUi.verticalSnapButton,
            self._mainUi.calibrateX1Button,
            self._mainUi.calibrateX2Button,
            self._mainUi.calibrateY1Button,
            self._mainUi.calibrateY2Button,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

        for button in [
            self._mainUi.zoomViewButton,
            self._mainUi.resetViewButton,
            self._mainUi.panViewButton,
            self._mainUi.selectViewButton,
            self._mainUi.swapXYButton,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

        for widget in [self._settingUi]:
            eff = QGraphicsDropShadowEffect(widget)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            widget.setGraphicsEffect(eff)

    # menu #############################################################
    def _pagingMVCInits(self):
        """
        Set up an instance of PageView.
        """
        self._pageButtons = {
            "calibrate": self._mainUi.modeSelectButton,
            "extract": self._mainUi.modeTagButton,
            "prefit": self._mainUi.modePrefitButton,
            "fit": self._mainUi.modeFitButton,
        }
        self._dataTransferButtons = {
            "prefit": self._mainUi.exportToPrefitButton,
            "fit": self._mainUi.exportToFitButton,
            "init": self._mainUi.pushButton_2,
        }
        self._pageStackedWidgets = {
            "center": self._mainUi.pagesStackedWidget,
            # "bottom": self.ui.bottomStackedWidget,
        }

        self._pageView = PageView(
            self._mainWindow,
            self._pageButtons, self._dataTransferButtons, self._pageStackedWidgets
        )

    # settings #########################################################
    def _settingsMVCInit(self):
        self._settingUi = SettingsWidget(self._mainWindow)
        self._settingsCtrl = SettingsCtrl(
            self._mainWindow,
            self._settingUi, 
            self._mainUi.settingsPushButton
        )

    # help button and gif tooltip ######################################
    def _helpButtonMVCInits(self):
        self._helpButtons = {
            "calibration": self._mainUi.calibrationHelpPushButton,
            "fit": self._mainUi.fitHelpPushButton,
            "numericalSpectrumSettings": self._settingUi.ui.numericalSpectrumSettingsHelpPushButton,
        }
        self._helpButtonCtrl = HelpButtonCtrl(self._mainWindow, self._helpButtons)

    # calibration ####################################
    ####################################################################
    def _calibrationMVCInits(self):
        """
        Set up an instance of CalibrationData and CalibrationView.
        """
        # ui grouping
        self._rawLineEdits = {
            "X1": self._mainUi.rawX1LineEdit,
            "X2": self._mainUi.rawX2LineEdit,
            "Y1": self._mainUi.rawY1LineEdit,
            "Y2": self._mainUi.rawY2LineEdit,
        }
        self._mapLineEdits = {
            "X1": self._mainUi.mapX1LineEdit,
            "X2": self._mainUi.mapX2LineEdit,
            "Y1": self._mainUi.mapY1LineEdit,
            "Y2": self._mainUi.mapY2LineEdit,
        }
        self._calibrationButtons = {
            "X1": self._mainUi.calibrateX1Button,
            "X2": self._mainUi.calibrateX2Button,
            "Y1": self._mainUi.calibrateY1Button,
            "Y2": self._mainUi.calibrateY2Button,
        }

        self._caliParamModel = CaliParamModel(self._mainWindow)
        self._calibrationView = CalibrationView(
            self._mainWindow,
            rawLineEdits=self._rawLineEdits,
            mapLineEdits=self._mapLineEdits,
            calibrationButtons=self._calibrationButtons,
        )

        self._calibrationCtrl = CalibrationCtrl(
            self._mainWindow,
            self._caliParamModel, self._calibrationView, self._pageButtons
        )

    # extract and tag ##################################################
    def _extractingMVCInits(self):
        """Set up the main class instances holding the data extracted from placing
        markers on the canvas. The AllExtractedData instance holds all data, whereas the
        ActiveExtractedData instance holds data of the currently selected data set."""
        # ui grouping: Labeling
        self._uiLabelBoxes = {
            "bare": self._mainUi.tagBareGroupBox,
            "dressed": self._mainUi.tagDressedGroupBox,
        }
        self._uiLabelRadioButtons = {
            "bare": self._mainUi.tagDispersiveBareRadioButton,
            "dressed": self._mainUi.tagDispersiveDressedRadioButton,
            "no tag": self._mainUi.noTagRadioButton,
        }
        self._uiBareLabelInputs = {
            "initial": self._mainUi.initialStateLineEdit,
            "final": self._mainUi.finalStateLineEdit,
            "photons": self._mainUi.phNumberBareSpinBox,
        }
        self._uiDressedLabelInputs = {
            "initial": self._mainUi.initialStateSpinBox,
            "final": self._mainUi.finalStateSpinBox,
            "photons": self._mainUi.phNumberDressedSpinBox,
        }
        # ui grouping: extracted data management
        self._uiExtractedDataManagements = {
            "new": self._mainUi.newRowButton,
            "delete": self._mainUi.deleteRowButton,
            "clear": self._mainUi.clearAllButton,
        }

        self._activeDataset = ActiveExtractedData(self._mainWindow)
        self._allDatasets = AllExtractedData(self._mainWindow)

        self._extractingView = ExtractingView(
            self._mainWindow,
            (
                self._uiLabelBoxes,
                self._uiLabelRadioButtons,
                self._uiBareLabelInputs,
                self._uiDressedLabelInputs,
                self._uiExtractedDataManagements,
                self._mainUi.datasetListView,
                self._mainUi.bareLabelOrder,
            ),
        )

        self._extractingCtrl = ExtractingCtrl(
            self._mainWindow,
            (self._allDatasets, self._activeDataset),
            self._extractingView,
        )

    # Pre-fit ##########################################################
    def _prefitMVCInits(self):
        # UI grouping
        self._prefitOptions = {
            "subsysToPlot": self._settingUi.ui.subsysComboBox,
            "initialState": self._settingUi.ui.initStateLineEdit,
            "photons": self._settingUi.ui.prefitPhotonSpinBox,
            "evalsCount": self._settingUi.ui.evalsCountLineEdit,
            "pointsAdded": self._settingUi.ui.pointsAddLineEdit,
            "autoRun": self._mainUi.autoRunCheckBox,
        }

        self._quantumModel = QuantumModel(self._mainWindow)

        self._prefitHSParams = PrefitHSParams(self._mainWindow)
        self._prefitCaliParams = PrefitCaliParams(self._mainWindow)
        self._prefitParamView = PrefitParamView(
            self._mainWindow,
            self._mainUi.prefitScrollAreaWidget,
            self._mainUi.prefitMinmaxScrollAreaWidget,
            self._mainUi.frame_prefit_minmax,
        )
        self._prefitView = PrefitView(
            self._mainWindow,
            runSweep=self._mainUi.plotButton,
            options=self._prefitOptions,
        )

        self._prefitCtrl = PrefitCtrl(
            self._mainWindow,
            (
                self._quantumModel, self._prefitHSParams, self._prefitCaliParams,
                self._allDatasets, self._caliParamModel, 
                self._measurementData, self._mainWindow
            ),
            (self._prefitView, self._prefitParamView, self._pageView),
        )

    # Fit ##############################################################
    def _fitMVCInits(self):
        # ui grouping
        self._fitOptions = {
            "tol": self._settingUi.ui.tolLineEdit,
            "optimizer": self._settingUi.ui.optimizerComboBox,
        }

        self._fitHSParams = FitHSParams(self._mainWindow)
        self._fitCaliParams = FitCaliParams(self._mainWindow)
        self._fitModel = FitModel(self._mainWindow)

        self._fitParamView = FitParamView(
            self._mainWindow,
            self._mainUi.fitScrollAreaWidget,
        )
        self._fitView = FitView(
            self._mainWindow,
            self._mainUi.fitButton,
            self._dataTransferButtons,
            self._fitOptions,
        )

        self._fitCtrl = FitCtrl(
            self._mainWindow,
            (
                self._fitModel, self._fitHSParams, self._fitCaliParams,
                self._prefitHSParams, self._prefitCaliParams, self._quantumModel,
                self._allDatasets, self._caliParamModel,
                self._measurementData
            ),
            (
                self._fitView, self._fitParamView, self._prefitParamView,
                self._pageView,
            ),
        )

    # plot #############################################################
    def _plottingMVCInits(self):
        # ui grouping
        self._measComboBoxes = {
            "x": self._mainUi.xComboBox,
            "y": self._mainUi.yComboBox,
            "z": self._mainUi.zComboBox,
        }
        self._measPlotSettings = {
            "topHat": self._settingUi.ui.topHatCheckBox,
            "wavelet": self._settingUi.ui.waveletCheckBox,
            "edge": self._settingUi.ui.edgeFilterCheckBox,
            "bgndX": self._settingUi.ui.bgndSubtractXCheckBox,
            "bgndY": self._settingUi.ui.bgndSubtractYCheckBox,
            "log": self._settingUi.ui.logScaleCheckBox,
            "min": self._settingUi.ui.rangeSliderMin,
            "max": self._settingUi.ui.rangeSliderMax,
            "color": self._settingUi.ui.colorComboBox,
        }
        self._canvasTools = {
            "reset": self._mainUi.resetViewButton,
            "zoom": self._mainUi.zoomViewButton,
            "pan": self._mainUi.panViewButton,
            "select": self._mainUi.selectViewButton,
            "snapX": self._mainUi.horizontalSnapButton,
            "snapY": self._mainUi.verticalSnapButton,
        }

        self._plottingCtrl = PlottingCtrl(
            self._mainWindow,
            self._mainUi.mplFigureCanvas,
            (
                self._measurementData,
                self._caliParamModel,
                self._allDatasets,
                self._activeDataset,
                self._quantumModel,
            ),
            (
                self._measComboBoxes,
                self._measPlotSettings,
                self._mainUi.swapXYButton,
                self._canvasTools,
                self._calibrationButtons,
                self._mainUi.calibratedCheckBox,
                self._pageView,
            ),
        )

    # IO ###############################################################
    def _IOMVCInits(self):
        self._registry = Registry()
        self._menuUi = MenuWidget(self._mainWindow)
        self._ioCtrl = IOCtrl(
            self._mainWindow,
            menuButton=self._mainUi.toggleMenuButton,
            menuUi=self._menuUi,
            registry=self._registry,
            mainWindow=self._mainWindow,
            fullDynamicalInit=self._dynamicalInit,
        )

    def _register(self):
        """
        register the entire app
        """
        # clear the registry
        self._registry.clear()

        # register the models
        self._registry.register(self._quantumModel.hilbertspace)
        self._registry.register(self._measurementData)
        self._registry.register(self._caliParamModel)
        self._registry.register(self._allDatasets)
        self._registry.register(self._prefitHSParams)
        self._registry.register(self._fitHSParams)
        self._registry.register(self._prefitCaliParams)
        self._registry.register(self._fitCaliParams)
        self._registry.register(self._mainWindow)

    # error message system #############################################
    def _statusMVCInits(self):
        self._statusModel = StatusModel(self._mainWindow)
        self._statusBarView = StatusBarView(
            self._mainWindow,
            self._mainUi.statusBar
        )
        self._statusCtrl = StatusCtrl(
            self._mainWindow,
            (
                self._quantumModel, self._fitModel, 
                self._fitHSParams, self._fitCaliParams
            ),
            self._statusModel,
            self._statusBarView,
        )