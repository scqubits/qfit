import numpy as np
from functools import partial

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import (
    QRunnable, QThreadPool, Signal, 
    QObject, QEventLoop, Slot
)

from qfit.utils.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.calibration_data import CalibrationData
from qfit.models.quantum_model_parameters import HSParamModel
from qfit.models.data_structures import QMFitParam
from qfit.models.status import StatusModel

class FitParamModel(HSParamModel[QMFitParam]):
    
    waitingForMSE = QEventLoop()
    fitThreadPool = QThreadPool()

    optimizer: str = "L-BFGS-B"
    tol: float = 1e-6

    mse: float = np.nan

    # signal & slots ===================================================
    @Slot()
    def updateOptimizer(self, optimizer: str):
        self.optimizer = optimizer

    @Slot()
    def updateTol(self, tol: str):
        self.tol = float(tol)

    @Slot()
    def MSECalculated(self, mse: float):
        self.mse = mse
        self.waitingForMSE.exit()

    # optimization setup ===============================================
    def _costFunction(
        self,
        paramDict: Dict[str, float],
    ) -> float:
        
        # use the parameter dictionary to update the parameter set
        # and their parent
        self.loadAttrDict(paramDict, "value")
        for parentName, parent in self.parameters.items():
            for paramName, _ in parent.items():
                self.updateParent(parentName, paramName)

        # update the hilbertspace & calibration function and wait for the result
        self.waitingForMSE.exec()

        # self.statusChanged.emit()
        return self.mse
    
    def setupOptimization(
        self,
    ) -> bool:
        # generate the fixed parameters and free parameter ranges
        fixed_params = {}
        free_param_ranges = {}
        param_dict = self.toParamDict()
        for key, params in param_dict.items():
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
                    # self.result.status_type = "ERROR"
                    # self.result.statusStrForView = (
                    #     "The minimum value of the "
                    #     "parameter is larger than the maximum value."
                    # )
                    return False
                if params.initValue < params.min or params.initValue > params.max:
                    # self.result.status_type = "ERROR"
                    # self.result.statusStrForView = (
                    #     "The initial value of the "
                    #     "parameter is not within the range defined by min and max."
                    # )
                    return False

        # set up the optimization
        try:
            self.opt = Optimization(
                fixed_params,
                free_param_ranges,
                self._costFunction,
                optimizer=self.optimizer,
                opt_options={
                    "disp": False,
                    "tol": self.tol,
                },
            )
        except:
            # self.result.status_type = "ERROR"
            # self.result.statusStrForView = "Fail to setup the optimization."
            return False

        return True
    
    # opt run ==========================================================
    # all of the below functions should be called after opt is set up
    def _initParams(self) -> Dict[str, float]:
        allInitParams = self.exportAttrDict("initValue")
        return {
            key: value
            for key, value in allInitParams.items()
            if key not in self.opt.fixed_variables.keys()
        }
    
    def _optCallback(
        self,
        paramDict: Dict[str, float],
        targetValue: float,
    ):
        self.loadAttrDict(paramDict, "value")
        self.mse = targetValue
        # self.statusChanged.emit()
        return

    def _paramHitBound(self) -> bool:
        for param_dict in self.parameters.values():
            for param in param_dict.values():
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
        # initial parameter & calculate the current MSE
        initParam = self._initParams()
        self._costFunction(initParam)

        runner = FitRunner(
            self.opt,
            initParam,
            self._optCallback,
        )
        self.fitThreadPool.start(runner)

        # if hit the boundary, raise warning
        if self._paramHitBound():
            # self.result.status_type = "WARNING"
            # self.result.statusStrForView = "The optimized parameters may hit the bound."
            return

        # # set the status
        # self.result.status_type = "SUCCESS"
        # self.result.statusStrForView = "Successfully optimized the parameter."

    


class FitRunner(QRunnable):
    def __init__(
        self,
        opt: Optimization,
        initParam: Dict[str, float],
        callback: Callable,
    ):
        super().__init__()
        
        self.opt = opt
        self.initParam = initParam
        self.callback = callback

    def run(self):
        self.opt.run(init_x=self.initParam, callback=self.callback)
        return
