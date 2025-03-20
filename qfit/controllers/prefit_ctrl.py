from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from qfit.models.parameter_set import SweepParamSet
from typing import Union, List, Dict, Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from qfit.models.prefit import PrefitHSParams, PrefitCaliParams
    from qfit.models.calibration import CaliParamModel
    from qfit.models.numerical_model import QuantumModel
    from qfit.models.status import StatusModel
    from qfit.models.extracted_data import AllExtractedData
    from qfit.models.measurement_data import MeasDataSet, MeasDataType
    from qfit.models.parameter_settings import ParameterType
    from qfit.views.prefit_view import SweepSettingsView, PrefitParamView
    from qfit.views.paging_view import PageView
    from qfit.core.mainwindow import MainWindow

    from scqubits.core.hilbert_space import HilbertSpace


class PrefitCtrl(QObject):
    """
    Controller for the prefit view. This class is responsible for
    connecting the prefit view with the quantum model and the prefit
    parameter model.

    Relevant UI elements:
    - sweepSettingsBiew: the view for sweep settings
    - prefitParamView: the parameter view
    - pageView: the page view

    Relevant models:
    - quantumModel: the quantum model
    - prefitHSParams: the prefit Hilbert space parameter model
    - prefitCaliParams: the prefit calibration parameter model
    - allDatasets: the extracted data model
    - caliParamModel: the calibration parameter model
    - measurementData: the measurement data model
    - mainWindow: the main window

    Parameters
    ----------
    parent : QObject
        The parent object
    models : Tuple[QuantumModel, PrefitHSParams, PrefitCaliParams, AllExtractedData, CaliParamModel, MeasDataSet, MainWindow]
    Views : Tuple[sweepSettingsView, PrefitParamView, PageView]
    """

    def __init__(
        self,
        parent: QObject,
        models: Tuple[
            "QuantumModel",
            "PrefitHSParams",
            "PrefitCaliParams",
            "AllExtractedData",
            "CaliParamModel",
            "MeasDataSet",
            "MainWindow",
        ],
        views: Tuple["SweepSettingsView", "PrefitParamView", "PageView"],
    ):
        super().__init__(parent)
        (
            self.quantumModel,
            self.prefitHSParams,
            self.prefitCaliParams,
            self.allDatasets,
            self.caliParamModel,
            self.measurementData,
            self.mainWindow,
        ) = models
        self.sweepSettingsView, self.prefitParamView, self.pageView = views

        self._switchFigConnects()
        self._quantumModelConnects()
        self._buttonConnects()
        self._sliderParamConnects()

    def replaceHS(
        self,
        hilbertspace: "HilbertSpace",
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.

        Parameters
        ----------
        hilbertSpace : HilbertSpace
            The HilbertSpace object.
        """
        self._buildHSParamSet(hilbertspace)
        self.sweepSettingsView.replaceHS(
            subsysNames=[
                SweepParamSet.parentSystemNames(subsys)
                for subsys in hilbertspace.subsystem_list[::-1]
            ],
        )
        self.quantumModel.replaceHS(hilbertspace)

    def replaceMeasData(self, measurementData: List["MeasDataType"]):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.

        Parameters
        ----------
        measurementData : List[MeasurementDataType]
            The measurement data.
        """
        self.quantumModel.replaceMeasData([data.name for data in measurementData])

    def dynamicalInit(
        self,
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views. In particular,
        parameter sets are built based on the HilbertSpace and the
        calibration model.

        Finally, it updates the view and the quantum model.
        """
        self._inheritCaliParams()

        self.prefitParamView.insertSliderMinMax(
            self.prefitHSParams.paramNamesDict(),
            self.prefitCaliParams.paramNamesDict(),
            removeExisting=True,
        )
        self.quantumModel.dynamicalInit()

        # update everything in the view
        self.prefitHSParams.emitUpdateBox()
        self.prefitHSParams.emitUpdateSlider()
        self.prefitCaliParams.emitUpdateBox()
        self.prefitCaliParams.emitUpdateSlider()
        for option, value in self.quantumModel.exportSweepOption().items():
            self.sweepSettingsView.setOptions(option, value)

        # update everything in the quantumModel
        self.prefitHSParams.emitHSUpdated()
        self.allDatasets.emitDataUpdated()
        self.caliParamModel.sendXCaliFunc()
        self.caliParamModel.sendYCaliFunc()

    def _switchFigConnects(self):
        """
        When the user switches between different measurement data figures,
        the spectrum displayed should be updated accordingly.
        """
        self.measurementData.figSwitched.connect(self.quantumModel.switchFig)

    def _quantumModelConnects(self):
        """
        Feed ingredients to the quantum model and update calculations.
        """
        self.prefitHSParams.hilbertSpaceUpdated.connect(
            self.quantumModel.updateHilbertSpace
        )
        self.allDatasets.dataUpdated.connect(self.quantumModel.updateExtractedData)
        self.caliParamModel.xCaliUpdated.connect(self.quantumModel.updateXCaliFunc)
        self.caliParamModel.yCaliUpdated.connect(self.quantumModel.updateYCaliFunc)
        self.measurementData.relimCanvas.connect(self.quantumModel.relimX)
        self.measurementData.updateRawXMap.connect(self.quantumModel.updateRawXMap)

        # connect the page change to the disable sweep
        self.pageView.pageChanged.connect(self.quantumModel.updateModeOnPageChange)

    def _buttonConnects(self):
        """
        Prefit option, the run sweep button --> quantum model.
        """
        self.sweepSettingsView.optionUpdated.connect(self.quantumModel.storeSweepOption)

        self.sweepSettingsView.runSweep.clicked.connect(
            lambda: self.quantumModel.updateCalc(forced=True)
        )

    def _sliderParamConnects(self):
        """
        Prefit parameter view --> prefit parameter model.
        (--> update HilbertSpace & calibration function in the quantum model)
        """
        # connect the HS & Cali parameters separately
        for signalSet, model in [
            (self.prefitParamView.HSSignals, self.prefitHSParams),
            (self.prefitParamView.caliSignals, self.prefitCaliParams),
        ]:
            signalSet: Dict[str, SignalInstance]
            model: Union[PrefitHSParams, PrefitCaliParams]

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

        # update hilbert space
        self.prefitParamView.HSEditingFinished.connect(
            self.prefitHSParams.updateParamForHS
        )

        # update cali model
        self.prefitParamView.caliEditingFinished.connect(
            self.prefitCaliParams.emitUpdateCaliModel
        )
        self.prefitCaliParams.updateCaliModel.connect(self.caliParamModel.setParamByPA)
        self.caliParamModel.updatePrefitModel.connect(
            self.prefitCaliParams.setParamByPA
        )

    def _buildHSParamSet(self, hilbertspace: "HilbertSpace"):
        """
        Identify prefit slider parameters for the HilbertSpace object. For
        now, we only accept one tunable parameter (flux or ng) in the
        HilbertSpace object. If one flux and one ng are found, we assume
        that the flux is swept.

        A temporary solution for the prefit slider parameter.
        """
        # check how many sweep parameters are found and create sliders
        # for the remaining parameters
        sweepParameterSet = SweepParamSet.initByHS(hilbertspace)
        param_types: set["ParameterType"] = set(
            sweepParameterSet.getFlattenedAttrDict("paramType").values()
        )

        if len(sweepParameterSet) == 0:
            print(
                "No sweep parameter (ng / flux) is found in the HilbertSpace "
                "object. Please check your quantum model."
            )
            self.mainWindow.close()

        else:
            # multiple sweep parameters are found, so we can create sliders
            # for the remaining parameters
            excluded: List[ParameterType] = ["cutoff", "truncated_dim", "l_osc"]
            self.prefitHSParams.dynamicalInit(
                hilbertspace=hilbertspace,
                excluded_parameter_type=(
                    excluded + list(param_types)  # exclude the sweep parameter
                ),
            )

    def _inheritCaliParams(
        self,
    ):
        # initialize calibration parameters
        self.prefitCaliParams.setAttrByParamSet(
            self.caliParamModel.toPrefitParams(),
            insertMissing=True,
        )
