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
    from qfit.views.prefit_view import PrefitParamView, SweepSettingsView
    from qfit.views.paging_view import PageView


class FitCtrl(QObject):
    """
    Controller for the fitting. This controller serves as a transmittor between
    the fitting parameters (model) and the fitting panel (view).

    Relevant UI elements:
    - fitting view
    - prefit view
    - page view

    Relevant model:
    - fitting parameters
    - prefit parameters
    - calibration parameters
    - quantum model
    - all extracted data
    - calibration parameter model
    - measurement data

    Parameters
    ----------
    parent : QObject
        The parent QObject.
    models : Tuple[FitModel, FitHSParams, FitCaliParams, PrefitHSParams,
        PrefitCaliParams, QuantumModel, AllExtractedData, CaliParamModel,
        MeasDataSet]
    views : Tuple[FitView, FitParamView, PrefitParamView, SweepSettingsView, PageView]
    """


    def __init__(
        self,
        parent: QObject,
        models: Tuple[
            "FitModel",
            "FitHSParams",
            "FitCaliParams",
            "PrefitHSParams",
            "PrefitCaliParams",
            "QuantumModel",
            "AllExtractedData",
            "CaliParamModel",
            "MeasDataSet",
        ],
        views: Tuple[
            "FitView",
            "FitParamView",
            "PrefitParamView",
            "SweepSettingsView",
            "PageView",
        ],
    ):
        super().__init__(parent)
        (
            self.fitModel,
            self.fitHSParams,
            self.fitCaliParams,
            self.prefitHSParams,
            self.prefitCaliParams,
            self.quantumModel,
            self.allDatasets,
            self.caliParamModel,
            self.measurementData,
        ) = models
        (
            self.fitView,
            self.fitParamView,
            self.prefitParamView,
            self.sweepSettingsView,
            self.pageView,
        ) = views
        
        self.OptTerminated = False

        self._optionConnects()
        self._tableParamConnects()
        self._fitCtrlConnects()

    def replaceHS(
        self,
        hilbertSpace: "HilbertSpace",
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.

        Parameters
        ----------
        hilbertSpace : HilbertSpace
            The HilbertSpace object.
        """
        self.fitHSParams.replaceHS(hilbertSpace)

    def dynamicalInit(self):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views. In particular, the
        fitting parameters are initialized with the prefit parameters.
        """
        # build paramset
        self.fitHSParams.setAttrByParamSet(
            self.prefitHSParams.toFitParams(),
            insertMissing=True,
        )
        # change this later to make it more safe
        self.fitHSParams.parentNameByObj = self.prefitHSParams.parentNameByObj
        self.fitHSParams.parentObjByName = self.prefitHSParams.parentObjByName

        self.fitCaliParams.setAttrByParamSet(
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
        table view --> parameter model
        """
        # update the value
        self.fitParamView.HSEditingFinished.connect(self.fitHSParams.storeParamAttr)
        self.fitParamView.CaliEditingFinished.connect(self.fitCaliParams.storeParamAttr)
        self.fitHSParams.updateBox.connect(self.fitParamView.setBoxValue)
        self.fitCaliParams.updateBox.connect(self.fitParamView.setBoxValue)

    def _optionConnects(self):
        """
        Connect the options for the fit
        """
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
        5. post optimization
        """
        # on buggon clicked: either run optimization or stop
        self.fitView.runFit.clicked.connect(self.onFitButtonClicked)

        # the prefit parameter export to fit
        self.fitView.dataTransferButtons["fit"].clicked.connect(self._prefitToFit)
        # the fit parameter export to prefit
        self.fitView.dataTransferButtons["prefit"].clicked.connect(self._resultToPrefit)

        # the final value to initial value
        self.fitView.dataTransferButtons["init"].clicked.connect(self._resultToInit)

        # post optimization
        self.fitModel.optFinished.connect(self.postOptimization)

    # slots ============================================================
    @Slot()
    def _prefitToFit(self):
        """
        Transfer the prefit parameters to fit parameters
        """
        self.fitHSParams.setAttrByParamSet(
            self.prefitHSParams.toFitParams(),
            attrsToUpdate=["min", "max", "initValue"],
            insertMissing=False,
        )
        self.fitCaliParams.setAttrByParamSet(
            self.caliParamModel.toFitParams(),
            attrsToUpdate=["min", "max", "initValue", "isFixed"],
            insertMissing=False,
        )

    @Slot()
    def _resultToPrefit(self):
        """
        Transfer the fitting result to prefit parameters and calibration parameters
        """
        self.caliParamModel.blockSignals(True)
        self.prefitHSParams.blockSignals(True)

        self.prefitHSParams.setAttrByParamSet(
            self.fitHSParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )
        self.prefitCaliParams.setAttrByParamSet(
            self.fitCaliParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )
        self.caliParamModel.setAttrByParamSet(
            self.fitCaliParams.toPrefitParams(),
            attrsToUpdate=["value"],
            insertMissing=False,
        )

        self.caliParamModel.blockSignals(False)
        self.prefitHSParams.blockSignals(False)

        self.caliParamModel.emitUpdateBox()
        self.prefitCaliParams.emitUpdateBox()
        self.prefitHSParams.emitUpdateBox()

        self.quantumModel.updateCalc()

    @Slot()
    def _resultToInit(self):
        """
        Transfer the fitting result to initial parameters
        """
        self.fitHSParams.setAttrByParamSet(
            self.fitHSParams.toInitParams(),
            attrsToUpdate=["initValue"],
            insertMissing=False,
        )
        self.fitCaliParams.setAttrByParamSet(
            self.fitCaliParams.toInitParams(),
            attrsToUpdate=["initValue"],
            insertMissing=False,
        )

    # optimization =====================================================
    def _paramTuningEnabled(self, enabled: bool):
        """
        Enable or disable the parameter tuning during the optimization
        """
        self.fitView.setEnabled(enabled)
        self.prefitParamView.sliderSet.setEnabled(enabled)
        self.sweepSettingsView.setEnabled(enabled)
        for page in ["calibrate", "extract", "prefit", "fit"]:
            self.pageView.setEnabled(enabled, page)

        # if not blocking the signal, the fit computation time will be
        # significantly longer
        self.caliParamModel.blockSignals(not enabled)

    @Slot()
    def userTerminateOptimization(self):
        """
        Terminate the optimization by the user. It is achieved by setting the
        OptTerminated flag to be True and the cost function will raise an
        exception.
        """
        self.OptTerminated = True

        # disable the fit button, forbid the user to click it again before
        # the optimization is actually terminated
        self.fitView.setFitButtonEnabled(False)

    @Slot()
    def onFitButtonClicked(self):
        """
        The slot for the fit button.
        If the mode is "run", start the optimization.
        If the mode is "stop", stop the optimization.
        """
        if self.fitView.fitButtonMode == "run":
            self.optimizeParams()
        else:
            self.userTerminateOptimization()

    def optimizeParams(self):
        """
        Set up and start the optimization:
        1. Check if the parameters are valid and the quantum model is ready
        2. Configure the models and views so that user cannot interact with them
        3. Set up the optimization with the fixed parameters, free parameter ranges,
            and cost function
        4. Start the optimization in a separate thread
        """
        if not self.fitHSParams.isValid:
            return

        if not self.quantumModel.readyToOpt:
            return

        # configure other models & views
        self._paramTuningEnabled(False)
        self.fitView.setFitButtonMode(mode="stop")

        # store a copy of the calibration parameters as we will change them
        # during the optimization, and we want to restore them afterward
        self.tmpCaliParams = self.caliParamModel.getFlattenedAttrDict("value")

        # setup the optimization
        self.fitHSParams.setAttrByParamSet(
            self.fitHSParams.initToFinalParams(), attrsToUpdate=["value"]
        )
        self.fitCaliParams.setAttrByParamSet(
            self.fitCaliParams.initToFinalParams(), attrsToUpdate=["value"]
        )
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
        Cook up a cost function for the optimization. It updates the quantum
        model and calibration model with the new parameters, and then returns
        the mean squared error of the spectrum.
        """
        if self.OptTerminated:
            raise Exception("Opt terminated by the user.")

        # update the hilbert space
        self.fitHSParams.setByFlattenedAttrDict(HSParams, "value")
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

        mse = self.quantumModel.updateCalc(forced=True)

        if mse is None or np.isnan(mse):
            raise ValueError("The cost function returns None or np.nan.")

        return mse

    def _optCallback(self, *args, **kwargs):
        """
        Callback for the optimization. It is called after each iteration of the
        optimization. It updates the views with the current parameters,
        current MSE and the current spectrum.
        """
        self.quantumModel.emitReadyToPlot()
        return self.quantumModel.sweep2SpecMSE(forced=True, sweepUsage="fit")

    @Slot()
    def postOptimization(self):
        """
        After the optimization is finished, restore the calibration parameters
        (as we used it to store the temporary parameters and update calibration
        functions), update the quantum model with the new parameters, and enable
        the parameter tuning.
        """
        self.OptTerminated = False

        # TODO: later, fit model will be able to update hspace
        self.caliParamModel.setByFlattenedAttrDict(self.tmpCaliParams, "value")

        # plot the spectrum again with new parameters
        tmp = self.quantumModel.sweepUsage
        self.quantumModel.sweepUsage = "fit-result"
        self.quantumModel.updateCalc(forced=True)
        self.quantumModel.sweepUsage = tmp

        self._paramTuningEnabled(True)
        # enable the fit button, update the mode to be run
        self.fitView.setFitButtonMode(mode="run")
        self.fitView.setFitButtonEnabled(True)
