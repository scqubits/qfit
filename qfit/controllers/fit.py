import numpy as np

from typing import List, Dict, Tuple, Callable, Union

from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.calibration_data import CalibrationData
from qfit.models.quantum_model_parameters import (
    QuantumModelFittingParameter,
    QuantumModelParameterSet,
)

class NumericalFitting():
    opt: Optimization

    def __init__(
        self,
    ):
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
        # print("para:", paramDict["fluxonium (Fluxonium).EL"])
        parameterSet.loadAttrDict(paramDict, "value")
        # print("actual EL:", parameterSet.parentObjByName["fluxonium (Fluxonium)"].EL)
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
    ):
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

    def _optCallback(
        self,
        freeParams: Dict[str, float],
        targetValue: float,
        parameterSet: QuantumModelParameterSet,
    ):
        # update the free parameters in the parameter set and display the target value

        parameterSet.loadAttrDict(freeParams, "value")
        print(targetValue**2)   # cost function is sqrt(MSE)
        
    def runOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
    ):
        """once the user clicks the optimize button, run the optimization"""


        # disable all the line edits, sliders, etc
        

        # initial parameter
        init_param_ui = parameterSet.exportAttrDict("initValue")
        init_param = {key: value for key, value in init_param_ui.items() 
                      if key not in self.opt.fixed_variables.keys()}

        try:
            traj = self.opt.run(
                init_x = init_param,
                callback = self._optCallback,
                callback_kwargs = {
                    "parameterSet": parameterSet,
                },
                # file_name = ...,
            )
        except AttributeError:
            # the optimization hasn't been set up yet
            return

        print(traj.final_full_para, traj.final_target**2)

        # display the results, optimizer's termination message
        # enable all the line edits, sliders, etc



