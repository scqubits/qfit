import numpy as np
from functools import partial

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import (
    QRunnable, QThreadPool, Signal, 
    QObject, QEventLoop, Slot
)

from scqubits.core.hilbert_space import HilbertSpace
from qfit.utils.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.parameter_set import (
    HSParamSet, ParamModelMixin, ParamSet,
)
from qfit.models.data_structures import FitParam, ParamAttr, SliderParam
from qfit.models.registry import RegistryEntry
from qfit.models.status import StatusModel


class FitParamModelMixin(ParamModelMixin[FitParam]):

    def _isValid(self, paramSet: ParamSet[FitParam]) -> bool:
        for key, params in paramSet.toParamDict().items():
            if params.min >= params.max:
                ###############
                # Error message
                ###############
                return False
            if not params.isFixed and (
                params.initValue < params.min or params.initValue > params.max
            ):
                ###############
                # Error message
                ###############
                return False
        return True
            
    def _fixedParams(self, paramSet: ParamSet[FitParam]) -> Dict[str, float]:
        return {
            key: params.initValue
            for key, params in paramSet.toParamDict().items()
            if params.isFixed
        }
        
    def _freeParamRanges(self, paramSet: ParamSet[FitParam]) -> Dict[str, List[float]]:
        return {
            key: [params.min, params.max]
            for key, params in paramSet.toParamDict().items()
            if not params.isFixed
        }
    
    def _initParams(self, paramSet: ParamSet[FitParam]) -> Dict[str, float]:
        return {
            key: params.initValue
            for key, params in paramSet.toParamDict().items()
        }
    
    def _toInitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[FitParam]:
        initParamSet = ParamSet[FitParam](FitParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                fitParam = FitParam(
                    name = paramName,           # useless
                    parent = param.parent,      # useless
                    paramType = param.paramType,# useless
                    initValue = param.value,     
                )
                initParamSet.insertParam(parentName, paramName, fitParam)

        return initParamSet
    
    def _toPrefitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[SliderParam]:
        prefitParamSet = ParamSet[SliderParam](SliderParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                sliderParam = SliderParam(
                    name = paramName,           # useless
                    parent = param.parent,      # useless
                    paramType = param.paramType,# useless
                    value = param.value,
                    min = -1,                   # useless
                    max = -1,                   # useless
                )
                prefitParamSet.insertParam(parentName, paramName, sliderParam)

        return prefitParamSet


class CombinedMeta(type(FitParamModelMixin), type(HSParamSet)):
    pass


class FitParamModel(
    HSParamSet[FitParam],
    FitParamModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = FitParam.attrToRegister

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        HSParamSet.__init__(self, FitParam)
        ParamModelMixin.__init__(self)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Not only set the parameter, but also emit the signal to update the view.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(parentName, name, attr, value)

        self._emitUpdateBox(self, parentName=parentName, paramName=name, attr=attr)

    @property
    def isValid(self) -> bool:
        return self._isValid(self)
            
    @property
    def fixedParams(self) -> Dict[str, float]:
        return self._fixedParams(self)
        
    @property
    def freeParamRanges(self) -> Dict[str, List[float]]:
        return self._freeParamRanges(self)
    
    @property
    def initParams(self) -> Dict[str, float]:
        return self._initParams(self)
    
    def toInitParams(self) -> ParamSet[FitParam]:
        return self._toInitParams(self)
    
    def toPrefitParams(self) -> ParamSet[SliderParam]:
        return self._toPrefitParams(self)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        return self._registerAll(self)

    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        super()._storeParamAttr(self, paramAttr, **kwargs)


class FitCaliModel(
    ParamSet[FitParam],
    FitParamModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = FitParam.attrToRegister

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        ParamSet.__init__(self, FitParam)
        ParamModelMixin.__init__(self)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Not only set the parameter, but also emit the signal to update the view.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(parentName, name, attr, value)

        self._emitUpdateBox(self, parentName=parentName, paramName=name, attr=attr)

    @property
    def isValid(self) -> bool:
        return self._isValid(self)
            
    @property
    def fixedParams(self) -> Dict[str, float]:
        return self._fixedParams(self)
        
    @property
    def freeParamRanges(self) -> Dict[str, List[float]]:
        return self._freeParamRanges(self)
    
    @property
    def initParams(self) -> Dict[str, float]:
        return self._initParams(self)
    
    def toInitParams(self) -> ParamSet[FitParam]:
        return self._toInitParams(self)
    
    def toPrefitParams(self) -> ParamSet[SliderParam]:
        return self._toPrefitParams(self)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        return self._registerAll(self)

    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        super()._storeParamAttr(self, paramAttr, **kwargs)


class FitModel(QObject):
    fitThreadPool = QThreadPool()

    optimizer: str = "L-BFGS-B"
    tol: float = 1e-6

    optFinished = Signal()

    # signal & slots ===================================================
    @Slot()
    def updateOptimizer(self, optimizer: str):
        self.optimizer = optimizer

    @Slot()
    def updateTol(self, tol: str):
        self.tol = float(tol)

    # optimization setup ===============================================
    def setupOptimization(
        self,
        fixedParams: Dict[str, float],
        freeParamRanges: Dict[str, List[float]],
        costFunction: Callable[[Dict[str, float]], float],
    ) -> bool:
        # set up the optimization
        try:
            self.opt = Optimization(
                fixedParams,
                freeParamRanges,
                costFunction,
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
    
    # def _optCallback(
    #     self,
    #     paramDict: Dict[str, float],
    #     targetValue: float,
    # ):
    #     self.loadAttrDict(paramDict, "value")
    #     self.mse = targetValue
    #     # self.statusChanged.emit()
    #     return

    def _paramHitBound(self, traj: OptTraj) -> bool:
        finalParam = traj.final_para
        for key, value in finalParam.items():
            freeRange = self.opt.free_variables[key]
            if value == freeRange[0] or value == freeRange[1]:
                return True
        return False

    @Slot(OptTraj)
    def _postOptimization(self, traj: OptTraj):
        self.optFinished.emit()

        if self._paramHitBound(traj):
            # self.result.status_type = "WARNING"
            # self.result.statusStrForView = "The optimized parameters may hit the bound."
            return

        # # set the status
        # self.result.status_type = "SUCCESS"
        # self.result.statusStrForView = "Successfully optimized the parameter."


    def runOptimization(
        self,
        initParam: Dict[str, float],
    ):
        """once the user clicks the optimize button, run the optimization"""
        # initial parameter & calculate the current MSE

        runner = FitRunner(
            self.opt,
            initParam,
            # self._optCallback,
        )
        runner.signalObj.optFinished.connect(self._postOptimization)
        self.fitThreadPool.start(runner)

    
class RunnerSignal(QObject):
    optFinished = Signal(OptTraj)


class FitRunner(QRunnable):

    signalObj = RunnerSignal()

    def __init__(
        self,
        opt: Optimization,
        initParam: Dict[str, float],
        # callback: Callable,
    ):
        super().__init__()
        
        self.opt = opt
        self.initParam = initParam
        # self.callback = callback

    def run(self):
        traj = self.opt.run(
            init_x=self.initParam, 
            # callback=self.callback
        )

        self.signalObj.optFinished.emit(traj)
