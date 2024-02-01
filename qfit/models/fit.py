import numpy as np

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject

from qfit.utils.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.calibration_data import CalibrationData
from qfit.models.quantum_model_parameters import (
    QuantumModelFittingParameter,
    QuantumModelParameterSet,
)
from qfit.models.status import StatusModel


# TODO need to check if NumericalFitting can inherit from QObject
class WorkerSignals(QObject):
    optInitFail = Signal()
    optFinished = Signal()
    statusChanged = Signal()


class NumericalFitting(QRunnable):
    opt: Optimization
    parameterSet: QuantumModelParameterSet

    def __init__(
        self,
    ):
        super().__init__()
        self.signals = WorkerSignals()
        return

    def setupUICallbacks(
        self,
        optimizerCallback: Callable,
        tolCallback: Callable,
    ):
        # set up callbacks for the UI
        self.optimizer = optimizerCallback
        self.tol = tolCallback
        return

    def _targetFunctionWrapper(
        self,
        paramDict: Dict[str, float],
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        extractedData: AllExtractedData,
        sweepParameterSet: QuantumModelParameterSet,
        calibrationData: CalibrationData,
    ):
        """
        A wrapper for the target function, which takes a dictionary of parameters and
        returns the square root of the MSE.
        """
        parameterSet.loadAttrDict(paramDict, "value")
        return np.sqrt(
            MSE(
                parameterSet,
                sweepParameterSet,
                calibrationData,
                extractedData,
            )
        )

    def setupOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        extractedData: AllExtractedData,
        sweepParameterSet: QuantumModelParameterSet,
        calibrationData: CalibrationData,
        result: StatusModel,
    ) -> bool:
        """
        Set up the optimization.

        Will return True if the optimization is successfully set up, False otherwise.

        """
        # store the things needed temporarily because the run() doesn't take any arguments
        self.parameterSet = parameterSet
        self.result = result

        # generate the fixed parameters and free parameter ranges
        fixed_params = {}
        free_param_ranges = {}
        param_dict = parameterSet.toParamDict()
        for key, params in param_dict.items():
            params: QuantumModelFittingParameter

            if params.isFixed or params.min == params.max:
                # min == max is actually not that rare, usually seen when
                # user wants to fix the parameter but don't know how to
                # fix it in the UI.
                # It's also possible that some parameter
                # with initial value 0 automatically gets min == max == 0.
                fixed_params[key] = params.initValue
            else:
                free_param_ranges[key] = [params.min, params.max]

                # check whether the values are valid
                if params.min > params.max:
                    self.result.status_type = "ERROR"
                    self.result.statusStrForView = (
                        "The minimum value of the "
                        "parameter is larger than the maximum value."
                    )
                    self.signals.optInitFail.emit()
                    return False
                if params.initValue < params.min or params.initValue > params.max:
                    self.result.status_type = "ERROR"
                    self.result.statusStrForView = (
                        "The initial value of the "
                        "parameter is not within the range defined by min and max."
                    )
                    self.signals.optInitFail.emit()
                    return False

        try:
            tol = float(self.tol())
        except ValueError:
            self.result.status_type = "ERROR"
            self.result.statusStrForView = "The tolerance should be a float."
            self.signals.optInitFail.emit()
            return False

        # set up the optimization
        try:
            self.opt = Optimization(
                fixed_params,
                free_param_ranges,
                self._targetFunctionWrapper,
                target_kwargs={
                    "parameterSet": parameterSet,
                    "MSE": MSE,
                    "extractedData": extractedData,
                    "sweepParameterSet": sweepParameterSet,
                    "calibrationData": calibrationData,
                },
                optimizer=self.optimizer(),
                opt_options={
                    "disp": False,
                    "tol": tol,
                },
            )
        except:
            self.result.status_type = "ERROR"
            self.result.statusStrForView = "Fail to setup the optimization."
            self.signals.optInitFail.emit()
            return False

        return True

    def _optCallback(
        self,
        freeParams: Dict[str, float],
        targetValue: float,
        parameterSet: QuantumModelParameterSet,
        result: StatusModel,
    ):
        # update the free parameters in the parameter set and display the target value

        parameterSet.loadAttrDict(freeParams, "value")
        result.newMseForComputingDelta = targetValue**2

    @staticmethod
    def _paramHitBound(parameterSet: QuantumModelParameterSet) -> bool:
        for param_dict in parameterSet.parameters.values():
            for param in param_dict.values():
                param: QuantumModelFittingParameter
                if param.isFixed:
                    continue
                if (
                    np.abs(param.value - param.min) < 1e-10
                    or np.abs(param.value - param.max) < 1e-10
                ):
                    return True
        return False

    def run(
        self,
    ):
        """once the user clicks the optimize button, run the optimization"""

        # initial parameter
        init_param_ui = self.parameterSet.exportAttrDict("initValue")
        init_param = {
            key: value
            for key, value in init_param_ui.items()
            if key not in self.opt.fixed_variables.keys()
        }

        # calculate the current MSE and display, also checks whether the target function can be calculated
        try:
            current_MSE = self.opt.target_w_free_var(init_param) ** 2
        except Exception as e:
            # will not be triggered by the users I think
            self.result.status_type = "ERROR"
            self.result.statusStrForView = (
                f"Fail to calculate MSE with {type(e).__name__}: {e}"
            )
            self.signals.optFinished.emit()
            return

        self.result.oldMseForComputingDelta = current_MSE
        self.result.newMseForComputingDelta = current_MSE
        self.result.status_type = "COMPUTING"

        try:
            traj = self.opt.run(
                init_x=init_param,
                callback=self._optCallback,
                callback_kwargs={
                    "parameterSet": self.parameterSet,
                    "result": self.result,
                },
                # file_name = ...,
            )
        except Exception as e:
            # will not be triggered by the users I think
            self.result.status_type = "ERROR"
            self.result.statusStrForView = (
                f"Fail to run the optimization with {type(e).__name__}: {e}"
            )
            self.signals.optFinished.emit()
            return

        # if hit the boundary, raise warning
        if self._paramHitBound(self.parameterSet):
            self.result.status_type = "WARNING"
            self.result.statusStrForView = "The optimized parameters may hit the bound."
            self.signals.optFinished.emit()
            return

        # set the status
        self.result.status_type = "SUCCESS"
        self.result.statusStrForView = "Successfully optimized the parameter."

        # emit the signal indicating the optimization is finished
        self.signals.optFinished.emit()
