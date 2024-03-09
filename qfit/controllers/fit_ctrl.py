from typing import Tuple, Dict, TYPE_CHECKING
from PySide6.QtCore import QObject, Slot
import numpy as np

if TYPE_CHECKING:
    from scqubits.core.hilbert_space import HilbertSpace
    from qfit.models.fit import FitModel, FitHSParams, FitCaliParams
    from qfit.models.prefit import PrefitHSParams, PrefitCaliParams
    from qfit.models.numerical_model import QuantumModel
    from qfit.models.extracted_data import AllExtractedData
    from qfit.models.calibration import CaliParamModel
    from qfit.models.measurement_data import MeasDataSet
    from qfit.views.fit_view import FitView, FitParamView
    from qfit.views.prefit_view import PrefitParamView
    from qfit.views.paging_view import PageView

class FitCtrl(QObject):
    def __init__(
        self, 
        parent: QObject,
        models: Tuple[
            "FitModel", "FitHSParams", "FitCaliParams", 
            "PrefitHSParams", "PrefitCaliParams", "QuantumModel",
            "AllExtractedData", "CaliParamModel", 
            "MeasDataSet"
        ], 
        views: Tuple[
            "FitView", "FitParamView", "PrefitParamView", 
            "PageView"
        ]
    ):
        super().__init__(parent)
        (
            self.fitModel, self.fitHSParams, self.fitCaliParams, 
            self.prefitHSParams, self.prefitCaliParams, self.quantumModel,
            self.allDatasets, self.caliParamModel, 
            self.measurementData, 
        ) = models
        (
            self.fitView, self.fitParamView, self.prefitParamView, 
            self.pageView
        ) = views

        self._optionConnects()
        self._tableParamConnects()
        self._fitCtrlConnects()

    def dynamicalInit(self, hilbertSpace: "HilbertSpace"):
        # build paramset
        self.fitHSParams.dynamicalInit(hilbertSpace)
        self.fitHSParams.setAttrByParamDict(
            self.prefitHSParams.toFitParams(),
            insertMissing=True,
        )
        # change this later to make it more safe
        self.fitHSParams.parentNameByObj = self.prefitHSParams.parentNameByObj
        self.fitHSParams.parentObjByName = self.prefitHSParams.parentObjByName

        self.fitCaliParams.setAttrByParamDict(
            self.caliParamModel.toFitParams(),
            insertMissing=True,
        )
        # insert parameters
        self.fitParamView.fitTableInserts(
            self.fitHSParams.paramNamesDict(),
            self.fitCaliParams.paramNamesDict(),
            removeExisting=True,
        )
        # like what happened with the prefit min max table, only after the table
        # is inserted, we can set the width of the column; reason unknown, only
        # happens on windows. TODO: investigate
        self.fitParamView.fitTableSet.setWidthOfColumn()

    # connections ======================================================
    def _tableParamConnects(self):
        """
        table --> parameter

        Note that in the current implementation, main window is both the
        controller and the model (hosting the parameterset)
        """
        # update the value
        self.fitParamView.HSEditingFinished.connect(self.fitHSParams.storeParamAttr)
        self.fitParamView.CaliEditingFinished.connect(self.fitCaliParams.storeParamAttr)
        self.fitHSParams.updateBox.connect(self.fitParamView.setBoxValue)
        self.fitCaliParams.updateBox.connect(self.fitParamView.setBoxValue)

    def _optionConnects(self):
        self.fitView.tolLineEdit.editingFinished.connect(
            lambda: self.fitModel.updateTol(self.fitView.tolLineEdit.value())
        )
        self.fitView.optimizerComboBox.currentIndexChanged.connect(
            lambda: self.fitModel.updateOptimizer(
                self.fitView.optimizerComboBox.currentText()
            )
        )

    def _fitCtrlConnects(self):
        """
        Connect the buttons for
        1. run fit
        2. parameters transfer: prefit to fit
        3. parameters transfer: fit to prefit
        4. parameters transfer: fit result to fit
        """
        # update hilbert space
        self.fitHSParams.hilbertSpaceUpdated.connect(
            self.quantumModel.updateHilbertSpace
        )

        # run optimization
        self.fitView.runFit.clicked.connect(self.optimizeParams)

        # the prefit parameter export to fit
        self.fitView.dataTransferButtons["fit"].clicked.connect(
            self._prefitToFit
        )
        # the fit parameter export to prefit
        self.fitView.dataTransferButtons["prefit"].clicked.connect(
            self._resultToPrefit
        )

        # the final value to initial value
        self.fitView.dataTransferButtons["init"].clicked.connect(
            self._resultToInit
        )

        # post optimization
        self.fitModel.optFinished.connect(self.postOptimization)

    # slots ============================================================
    @Slot()
    def _prefitToFit(self):
        self.fitHSParams.setAttrByParamDict(
            self.prefitHSParams.toFitParams(),
            attrsToUpdate=["value", "min", "max", "initValue"],
            insertMissing=False,
        )
        self.fitCaliParams.setAttrByParamDict(
            self.caliParamModel.toFitParams(),
            attrsToUpdate=["value", "min", "max", "initValue", "isFixed"],
            insertMissing=False,
        )

    @Slot()
    def _resultToPrefit(self):
        self.caliParamModel.blockSignals(True)
        self.prefitHSParams.blockSignals(True)

        self.prefitHSParams.setAttrByParamDict(
            self.fitHSParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )
        self.prefitCaliParams.setAttrByParamDict(
            self.fitCaliParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )
        self.caliParamModel.setAttrByParamDict(
            self.fitCaliParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )

        self.caliParamModel.blockSignals(False)
        self.prefitHSParams.blockSignals(False)

        self.quantumModel.updateCalc()

    @Slot()
    def _resultToInit(self):
        self.fitHSParams.setAttrByParamDict(
            self.fitHSParams.toInitParams(),
            attrsToUpdate=["initValue"],
            insertMissing=False,
        )
        self.fitCaliParams.setAttrByParamDict(
            self.fitCaliParams.toInitParams(),
            attrsToUpdate=["initValue"],
            insertMissing=False,
        )

    # optimization =====================================================
    @Slot()
    def optimizeParams(self):
        if not self.fitHSParams.isValid:
            return

        # configure other models & views
        self.fitView.runFit.setEnabled(False)
        self.prefitParamView.sliderSet.setEnabled(False)
        # it seems that even though the sweep is disabled while changing
        # the parameters, the signals are still able to reach the quantumModel
        # and trigger the calculation. So we need to block the signals
        self.fitHSParams.blockSignals(True)
        self.caliParamModel.blockSignals(True)

        # store a copy of the calibration parameters as we will change them
        # during the optimization, and we want to restore them afterward
        self.tmpCaliParams = self.caliParamModel.getFlattenedAttrDict("value")

        # setup the optimization
        self.fitModel.setupOptimization(
            HSFixedParams=self.fitHSParams.fixedParams,
            HSFreeParamRanges=self.fitHSParams.freeParamRanges,
            caliFixedParams=self.fitCaliParams.fixedParams,
            caliFreeParamRanges=self.fitCaliParams.freeParamRanges,
            costFunction=self._costFunction,
        )

        # cook up a cost function
        self.fitModel.runOptimization(
            initParam=self.fitHSParams.initParams,
            callback=self._optCallback,
        )

    def _costFunction(
        self, HSParams: Dict[str, float], caliParams: Dict[str, float]
    ) -> float:
        """
        Cook up a cost function for the optimization
        """
        self.quantumModel.disableSweep = True

        # update the hilbert space
        self.fitHSParams.setByFlattenedAttrDict(HSParams, "value")  # display the value
        # self.prefitHSParams.setByAttrDict(HSParams, "value")  # update HS
        self.fitHSParams.updateParamForHS()
        self.quantumModel.updateHilbertSpace(self.fitHSParams.hilbertspace)

        # update the calibration
        self.caliParamModel.setByFlattenedAttrDict(caliParams, "value")
        self.fitCaliParams.setByFlattenedAttrDict(caliParams, "value")
        self.quantumModel.updateXCaliFunc(self.caliParamModel.XCalibration())
        self.quantumModel.updateYCaliFunc(
            self.caliParamModel.YCalibration(),
            self.caliParamModel.invYCalibration(),
        )

        self.quantumModel.disableSweep = False

        mse = self.quantumModel.updateCalc()

        if mse is None or np.isnan(mse):
            raise ValueError("The cost function returns None or np.nan.")

        return mse

    def _optCallback(self, *args, **kwargs):
        self.quantumModel.emitReadyToPlot()
        return self.quantumModel.sweep2SpecMSE()

    @Slot()
    def postOptimization(self):
        # TODO: later, fit model will be able to update hspace
        self.caliParamModel.setByFlattenedAttrDict(
            self.tmpCaliParams, "value"
        )

        # plot the spectrum
        tmp = self.quantumModel.sweepUsage
        self.quantumModel.sweepUsage = "fit-result"
        self.quantumModel.updateCalc()
        self.quantumModel.sweepUsage = tmp

        self.fitView.runFit.setEnabled(True)
        self.prefitParamView.sliderSet.setEnabled(True)
        self.fitHSParams.blockSignals(False)
        self.caliParamModel.blockSignals(False)