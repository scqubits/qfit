from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from qfit.models.parameter_set import SweepParamSet
from typing import Union, List, Dict, Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from qfit.models.prefit import PrefitParamModel, PrefitCaliModel
    from qfit.models.calibration import CaliParamModel
    from qfit.models.numerical_model import QuantumModel
    from qfit.models.status import StatusModel
    from qfit.models.extracted_data import AllExtractedData
    from qfit.models.measurement_data import MeasDataSet, MeasurementDataType
    from qfit.models.parameter_settings import ParameterType
    from qfit.views.prefit_view import PrefitView, PrefitParamView
    from qfit.views.paging_view import PageView
    from qfit.core.mainwindow import MainWindow

    from scqubits.core.hilbert_space import HilbertSpace


class PrefitCtrl(QObject):
    def __init__(
        self, 
        models: Tuple[
            "QuantumModel", "PrefitParamModel", "PrefitCaliModel",
            "AllExtractedData", "CaliParamModel",
            "MeasDataSet", "MainWindow"
        ],
        views: Tuple["PrefitView", "PrefitParamView", "PageView"],
    ):
        super().__init__()
        (
            self.quantumModel, self.prefitParamModel, self.prefitCaliModel, 
            self.allDatasets, self.caliParamModel,
            self.measurementData, self.mainWindow
        ) = models
        self.prefitView, self.prefitParamView, self.pageView = views

        self._quantumModelConnects()
        self._buttonConnects()
        self._sliderParamConnects()

    def dynamicalInit(
        self, 
        hilbertspace: "HilbertSpace", 
        measurementData: List["MeasurementDataType"]
    ):
        self._buildParamSet(hilbertspace)
        self.prefitView.dynamicalInit(
            subsysNames=[
                SweepParamSet.parentSystemNames(subsys)
                for subsys in hilbertspace.subsystem_list[::-1]
            ],
        )
        self.prefitParamView.insertSliderMinMax(
            self.prefitParamModel.paramNamesDict(),
            self.prefitCaliModel.paramNamesDict(),
            removeExisting=True,
        )

        self.quantumModel.dynamicalInit(
            hilbertspace, [data.name for data in measurementData]
        )

        # update everything in the view
        self.prefitParamModel.emitUpdateBox()
        self.prefitParamModel.emitUpdateSlider()
        self.prefitCaliModel.emitUpdateBox()
        self.prefitCaliModel.emitUpdateSlider()
        for option, value in self.quantumModel.exportSweepOption().items():
            self.prefitView.setOptions(option, value)

        # update everything in the quantumModel
        self.quantumModel.disableSweep = True  # disable the auto sweep
        self.prefitParamModel.emitHSUpdated()
        self.allDatasets.emitDataUpdated()
        self.caliParamModel.sendXCaliFunc()
        self.caliParamModel.sendYCaliFunc()

    def _quantumModelConnects(self):
        self.prefitParamModel.hilbertSpaceUpdated.connect(
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
        self.prefitView.optionUpdated.connect(self.quantumModel.storeSweepOption)

        self.prefitView.runSweep.clicked.connect(
            lambda: self.quantumModel.updateCalc(calledByPlotButton=True)
        )

    def _sliderParamConnects(self):
        """
        View --> model: slider --> parameter

        Note that in the current implementation, main window is both the
        controller and the model (hosting the parameterset)
        """
        # connect the HS & Cali parameters separately
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
            # signalSet["sliderChanged"].connect(
            #     lambda paramAttr, model=model: print(model, "slider changed")
            # )
            signalSet["textChanged"].connect(
                lambda paramAttr, model=model: model.storeParamAttr(paramAttr)
            )
            signalSet["rangeEditingFinished"].connect(
                lambda paramAttr, model=model: model.storeParamAttr(paramAttr)
            )
            # signalSet["rangeEditingFinished"].connect(
            #     lambda paramAttr, model=model: print(model, "range editing finished")
            # )

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
            self.prefitParamModel.updateParent
        )
        self.pageView.pageChanged.connect(
            lambda page: self.prefitParamModel.updateAllParents() if page == "prefit" else None
        )

        # update cali model
        self.prefitParamView.caliEditingFinished.connect(
            self.prefitCaliModel.emitUpdateCaliModel
        )
        self.prefitCaliModel.updateCaliModel.connect(self.caliParamModel.setParamByPA)
        self.caliParamModel.updatePrefitModel.connect(self.prefitCaliModel.setParamByPA)

    def _buildParamSet(self, hilbertspace: "HilbertSpace"):
        """
        identify prefit slider parameters. A temporary solution for the
        prefit slider parameter.
        """
        # check how many sweep parameters are found and create sliders
        # for the remaining parameters
        sweepParameterSet = SweepParamSet.initByHS(hilbertspace)
        param_types: set["ParameterType"] = set(
            sweepParameterSet.getAttrDict("paramType").values()
        )

        if len(sweepParameterSet) == 0:
            print(
                "No sweep parameter (ng / flux) is found in the HilbertSpace "
                "object. Please check your quantum model."
            )
            self.mainWindow.close()

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
            self.mainWindow.close()

        # initialize calibration sliders
        self.prefitCaliModel.setAttrByParamDict(
            self.caliParamModel.toPrefitParams(),
            insertMissing=True,
        )