import numpy as np

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject

from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.calibration_data import CalibrationData
from qfit.models.quantum_model_parameters import (
    QuantumModelFittingParameter,
    QuantumModelParameterSet,
)
from qfit.models.status_result_data import Result

class WorkerSignals(QObject):
    optFinished = Signal()

class NumericalFitting(QRunnable):
    opt: Optimization
    parameterSet: QuantumModelParameterSet

    def __init__(
        self,
    ):
        super().__init__()
        self.signals = WorkerSignals()
        return

    def setupUICallbacks(self):
        # set up callbacks for the UI
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
        return np.sqrt(MSE(
            parameterSet, 
            sweepParameterSet,
            calibrationData,
            extractedData, 
        ))
    
    
    def setupOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        extractedData: AllExtractedData,
        sweepParameterSet: QuantumModelParameterSet,
        calibrationData: CalibrationData,
        result: Result,
    ):
        # store the things needed temporarily because the run() doesn't take any arguments
        self.parameterSet = parameterSet
        self.result = result

        # generate the fixed parameters and free parameter ranges
        fixed_params = {}
        free_param_ranges = {}
        param_dict = parameterSet.toParamDict()
        for key, params in param_dict.items():
            params: QuantumModelFittingParameter
            if params.isFixed:
                fixed_params[key] = params.initValue
            else:
                free_param_ranges[key] = [params.min, params.max]


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
                optimizer="L-BFGS-B",
                opt_options={
                    "disp": True,
                }
            )
        except:
            self.result.status_type = "ERROR"
            self.result.status_text = "Fail to setup the optimization."
            self.signals.optFinished.emit()

    def _optCallback(
        self,
        freeParams: Dict[str, float],
        targetValue: float,
        parameterSet: QuantumModelParameterSet,
        result: Result
    ):
        # update the free parameters in the parameter set and display the target value

        parameterSet.loadAttrDict(freeParams, "value")
        result.current_mse = targetValue**2

    @staticmethod
    def _paramHitBound(parameterSet) -> bool:
        for param_dict in parameterSet.parameters.values():
            for param in param_dict.values():
                param: QuantumModelFittingParameter
                if (np.abs(param.value - param.min) < 1e-10 
                    or np.abs(param.value - param.max) < 1e-10):
                    return True
        return False

    def run(
        self,
    ):
        """once the user clicks the optimize button, run the optimization"""

        # initial parameter
        init_param_ui = self.parameterSet.exportAttrDict("initValue")
        init_param = {key: value for key, value in init_param_ui.items() 
                      if key not in self.opt.fixed_variables.keys()}
        
        # calculate the current MSE and display, also checks whether the target function can be calculated
        try:
            current_MSE = self.opt.target_w_free_var(init_param)**2
        except Exception as e:
            # will not be triggered by the users I think
            self.result.status_type = "ERROR"
            self.result.status_text = f"Fail to calculate MSE with {type(e).__name__}: {e}"
            self.signals.optFinished.emit()
            return
        
        self.result.previous_mse = current_MSE
        self.result.current_mse = current_MSE
        self.result.status_type = "COMPUTING"

        try:
            traj = self.opt.run(
                init_x = init_param,
                callback = self._optCallback,
                callback_kwargs = {
                    "parameterSet": self.parameterSet,
                    "result": self.result,
                },
                # file_name = ...,
            )
        except Exception as e:
            # will not be triggered by the users I think
            self.result.status_type = "ERROR"
            self.result.status_text = f"Fail to run the optimization with {type(e).__name__}: {e}"
            self.signals.optFinished.emit()
            return
        
        # if hit the boundary, raise error
        if self._paramHitBound(self.parameterSet):
            self.result.status_type = "WARNING"
            self.result.status_text = "The optimized parameters may hit the bound."
            self.signals.optFinished.emit()
            return
    
        # set the status
        self.result.status_type = "SUCCESS"
        self.result.status_text = "Successfully optimized the parameter."

        # emit the signal indicating the optimization is finished
        self.signals.optFinished.emit()




