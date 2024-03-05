from typing import Tuple, Dict, TYPE_CHECKING
from PySide6.QtCore import QObject, Slot
import numpy as np

if TYPE_CHECKING:
    from qfit.models.fit import FitModel, FitParamModel, FitCaliModel
    from qfit.models.prefit import PrefitParamModel, PrefitCaliModel
    from qfit.models.numerical_model import QuantumModel
    from qfit.models.status import StatusModel
    from qfit.models.extracted_data import AllExtractedData
    from qfit.models.calibration import CaliParamModel
    from qfit.models.measurement_data import MeasDataSet
    from qfit.views.fit_view import FitView, FitParamView
    from qfit.views.prefit_view import PrefitParamView

class FitCtrl(QObject):
    def __init__(
        self, 
        models: Tuple[
            "FitModel", "FitParamModel", "FitCaliModel", 
            "PrefitParamModel", "PrefitCaliModel", "QuantumModel",
            "AllExtractedData", "CaliParamModel", 
            "MeasDataSet"
        ], 
        views: Tuple["FitView", "FitParamView", "PrefitParamView"]
    ):
        super().__init__()
        (
            self.fitModel, self.fitParamModel, self.fitCaliModel, 
            self.prefitParamModel, self.prefitCaliModel, self.quantumModel,
            self.allDatasets, self.caliParamModel, 
            self.measurementData, 
        ) = models
        self.fitView, self.fitParamView, self.prefitParamView = views

        self._optionConnects()
        self._tableParamConnects()
        self._fitCtrlConnects()

    def dynamicalInit(self):
        # build paramset
        self.fitParamModel.setAttrByParamDict(
            self.prefitParamModel.toFitParams(),
            insertMissing=True,
        )
        self.fitCaliModel.setAttrByParamDict(
            self.caliParamModel.toFitParams(),
            insertMissing=True,
        )
        # insert parameters
        self.fitParamView.fitTableInserts(
            self.fitParamModel.paramNamesDict(),
            self.fitCaliModel.paramNamesDict(),
            removeExisting=True,
        )
        # like what happened with the prefit min max table, only after the table
        # is inserted, we can set the width of the column; reason unknown, only
        # happens on windows. TODO: investigate
        self.fitParamView.fitTableSet.setWidthOfColumn()

    def _tableParamConnects(self):
        """
        table --> parameter

        Note that in the current implementation, main window is both the
        controller and the model (hosting the parameterset)
        """
        # update the value
        self.fitParamView.HSEditingFinished.connect(self.fitParamModel.storeParamAttr)
        self.fitParamView.CaliEditingFinished.connect(self.fitCaliModel.storeParamAttr)
        self.fitParamModel.updateBox.connect(self.fitParamView.setBoxValue)
        self.fitCaliModel.updateBox.connect(self.fitParamView.setBoxValue)

    def _costFunction(
        self, HSParams: Dict[str, float], caliParams: Dict[str, float]
    ) -> float:
        """
        Cook up a cost function for the optimization
        """
        self.quantumModel.disableSweep = True

        # update the hilbert space
        self.fitParamModel.setByAttrDict(HSParams, "value")  # display the value
        self.prefitParamModel.setByAttrDict(HSParams, "value")  # update HS
        for params in self.prefitParamModel.values():
            for p in params.values():
                p.setParameterForParent()
        self.quantumModel.updateHilbertSpace(self.prefitParamModel.hilbertspace)

        # update the calibration
        self.caliParamModel.setByAttrDict(caliParams, "value")
        self.fitCaliModel.setByAttrDict(caliParams, "value")
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
    def optimizeParams(self):
        if not self.fitParamModel.isValid:
            return

        # configure other models & views
        self.fitView.runFit.setEnabled(False)
        self.prefitParamView.sliderSet.setEnabled(False)
        # it seems that even though the sweep is disabled while changing
        # the parameters, the signals are still able to reach the quantumModel
        # and trigger the calculation. So we need to block the signals
        self.prefitParamModel.blockSignals(True)
        self.caliParamModel.blockSignals(True)

        # TODO: later, fit model will be able to update hspace
        # and we don't need to store the prefit parameters
        self.tmpPrefitParams = self.prefitParamModel.getAttrDict("value")
        self.tmpCaliParams = self.caliParamModel.getAttrDict("value")

        # setup the optimization
        self.fitModel.setupOptimization(
            HSFixedParams=self.fitParamModel.fixedParams,
            HSFreeParamRanges=self.fitParamModel.freeParamRanges,
            caliFixedParams=self.fitCaliModel.fixedParams,
            caliFreeParamRanges=self.fitCaliModel.freeParamRanges,
            costFunction=self._costFunction,
        )

        # cook up a cost function
        self.fitModel.runOptimization(
            initParam=self.fitParamModel.initParams,
            callback=self._optCallback,
        )

    @Slot()
    def postOptimization(self):
        self.fitView.runFit.setEnabled(True)
        self.prefitParamView.sliderSet.setEnabled(True)
        self.prefitParamModel.blockSignals(False)
        self.caliParamModel.blockSignals(False)

        # TODO: later, fit model will be able to update hspace
        self.prefitParamModel.setByAttrDict(
            self.tmpPrefitParams, "value"
        )
        self.caliParamModel.setByAttrDict(
            self.tmpCaliParams, "value"
        )

        # plot the spectrum
        tmp = self.quantumModel.sweepUsage
        self.quantumModel.sweepUsage = "fit-result"
        self.quantumModel.updateCalc()
        self.quantumModel.sweepUsage = tmp

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
        # run optimization
        self.fitView.runFit.clicked.connect(self.optimizeParams)

        # the prefit parameter export to fit
        self.fitView.dataTransferButtons["prefit"].clicked.connect(
            lambda: self.fitParamModel.setAttrByParamDict(
                self.prefitParamModel.toFitParams(),
                attrsToUpdate=["value", "min", "max", "initValue"],
                insertMissing=False,
            )
        )
        self.fitView.dataTransferButtons["prefit"].clicked.connect(
            lambda: self.fitCaliModel.setAttrByParamDict(
                self.caliParamModel.toFitParams(),
                attrsToUpdate=["value", "min", "max", "initValue", "isFixed"],
                insertMissing=False,
            )
        )
        # the fit parameter export to prefit
        self.fitView.dataTransferButtons["fit"].clicked.connect(
            lambda: self.prefitParamModel.setAttrByParamDict(
                self.fitParamModel.toPrefitParams(),
                attrsToUpdate=["value"],
                insertMissing=False,
            )
        )
        self.fitView.dataTransferButtons["fit"].clicked.connect(
            lambda: self.prefitCaliModel.setAttrByParamDict(
                self.fitCaliModel.toPrefitParams(),
                attrsToUpdate=["value"],
                insertMissing=False,
            )
        )
        self.fitView.dataTransferButtons["fit"].clicked.connect(
            lambda: self.caliParamModel.setAttrByParamDict(
                self.fitCaliModel.toPrefitParams(),
                attrsToUpdate=["value"],
                insertMissing=False,
            )
        )

        # the final value to initial value
        self.fitView.dataTransferButtons["init"].clicked.connect(
            lambda: self.fitParamModel.setAttrByParamDict(
                self.fitParamModel.toInitParams(),
                attrsToUpdate=["initValue"],
                insertMissing=False,
            )
        )
        self.fitView.dataTransferButtons["init"].clicked.connect(
            lambda: self.fitCaliModel.setAttrByParamDict(
                self.fitCaliModel.toInitParams(),
                attrsToUpdate=["initValue"],
                insertMissing=False,
            )
        )

        # post optimization
        self.fitModel.optFinished.connect(self.postOptimization)