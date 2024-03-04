import numpy as np
from functools import partial

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, QEventLoop, Slot

from scqubits.core.hilbert_space import HilbertSpace
from qfit.utils.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.parameter_set import (
    ParamSet,
    ParamModelMixin,
    ParamSet,
)
from qfit.models.data_structures import FitParam, ParamAttr, SliderParam, ParamBase
from qfit.models.registry import RegistryEntry
from qfit.models.status import StatusModel

from qfit.models.data_structures import Status


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
            if not params.isFixed
        }

    def _toInitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[FitParam]:
        initParamSet = ParamSet[FitParam](FitParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                fitParam = FitParam(
                    name=paramName,  # useless
                    parent=param.parent,  # useless
                    paramType=param.paramType,  # useless
                    initValue=param.value,
                )
                initParamSet.insertParam(parentName, paramName, fitParam)

        return initParamSet

    def _toPrefitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[ParamBase]:
        prefitParamSet = ParamSet[ParamBase](ParamBase)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                sliderParam = ParamBase(
                    name=paramName,  # useless
                    parent=param.parent,  # useless
                    paramType=param.paramType,  # useless
                    value=param.value,
                )
                prefitParamSet.insertParam(parentName, paramName, sliderParam)

        return prefitParamSet


class CombinedMeta(type(FitParamModelMixin), type(ParamSet)):
    pass


class FitParamModel(
    ParamSet[FitParam],
    FitParamModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = FitParam.dataAttr

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

    def toPrefitParams(self) -> ParamSet[ParamBase]:
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
    attrs = FitParam.dataAttr

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

    def toPrefitParams(self) -> ParamSet[ParamBase]:
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
    updateStatus = Signal(Status)

    HSParamNames: List[str] = []
    iteration: int = 0
    status: Status

    def __init__(self):
        super().__init__()

        FitRunner.signalHoster.optFinished.connect(self._postOptimization)

    # signal & slots ===================================================
    @Slot()
    def updateOptimizer(self, optimizer: str):
        self.optimizer = optimizer

    @Slot()
    def updateTol(self, tol: str):
        self.tol = float(tol)

    @Slot()
    def resetIteration(self):
        self.iteration = 0

    # optimization setup ===============================================
    def _costWrapper(
        self,
        func: Callable[[Dict[str, float], Dict[str, float]], float],
    ):
        def costWrapper(
            paramDict: Dict[str, float],
        ) -> float:
            HSParams = {
                key: value
                for key, value in paramDict.items()
                if key in self.HSParamNames
            }
            caliParams = {
                key: value
                for key, value in paramDict.items()
                if key not in self.HSParamNames
            }

            return func(HSParams, caliParams)

        return costWrapper

    def _callbackWrapper(
        self,
        callback: Callable,
    ) -> Callable:
        """
        return a wrapped callback function which is used to update the status
        """

        def wrappedCallback(*args, **kwargs):
            mse = callback(*args, **kwargs)
            self.iteration += 1
            # status update; during the optimization, the status is always computing
            status = Status(
                statusSource="fit",
                statusType="computing",
                message="",
                mse=mse,  # a dummy value
            )
            self.updateStatus.emit(status)

        return wrappedCallback

    def setupOptimization(
        self,
        HSFixedParams: Dict[str, float],
        HSFreeParamRanges: Dict[str, List[float]],
        caliFixedParams: Dict[str, float],
        caliFreeParamRanges: Dict[str, List[float]],
        costFunction: Callable[[Dict[str, float], Dict[str, float]], float],
    ) -> bool:
        # distinguish between HS and cali parameters
        self.HSParamNames = list(HSFixedParams.keys()) + list(HSFreeParamRanges.keys())

        # set up the optimization
        try:
            self.opt = Optimization(
                HSFixedParams | caliFixedParams,
                HSFreeParamRanges | caliFreeParamRanges,
                self._costWrapper(costFunction),
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
    def _postOptimization(self, traj: Union[OptTraj, str]):
        self.optFinished.emit()
        # reset iteration
        self.iteration = 0

        if isinstance(traj, str):
            status = Status(
                statusSource="fit",
                statusType="error",
                message="Fail to optimize the parameter. Due to the "
                        "following reason: " + traj,
                mse=np.nan,
            )
            self.updateStatus.emit(status)
            return
        

        if self._paramHitBound(traj):
            status = Status(
                statusSource="fit",
                statusType="warning",
                message="The optimized parameters may hit the bound.",
                mse=traj.final_target,
            )
            self.updateStatus.emit(status)
            return

        # # set the status
        # self.result.status_type = "SUCCESS"
        # self.result.statusStrForView = "Successfully optimized the parameter."
        status = Status(
            statusSource="fit",
            statusType="success",
            message="Successfully optimized the parameter.",
            mse=traj.final_target,
        )
        self.updateStatus.emit(status)

    def runOptimization(
        self,
        initParam: Dict[str, float],
        callback: Callable,
    ):
        """once the user clicks the optimize button, run the optimization"""
        # initial parameter & calculate the current MSE
        initMSE = self.opt.target_func(initParam)
        # status update
        status = Status(
            statusSource="fit",
            statusType="initializing",
            message="",
            mse=initMSE,
        )
        self.updateStatus.emit(status)

        print("Runner starts.")
        runner = FitRunner(
            self.opt,
            initParam,
            self._callbackWrapper(callback),
        )
        self.fitThreadPool.start(runner)


class RunnerSignal(QObject):
    optFinished = Signal(OptTraj)


class FitRunner(QRunnable):

    signalHoster = RunnerSignal()

    def __init__(
        self,
        opt: Optimization,
        initParam: Dict[str, float],
        callback: Callable,
    ):
        super().__init__()
        print("Runner inits.", self)

        self.opt = opt
        self.initParam = initParam
        self.callback = callback

    def run(self):
        try:
            traj = self.opt.run(init_x=self.initParam, callback=self.callback)
        except Exception as e:
            self.signalHoster.optFinished.emit(str(e))

        self.signalHoster.optFinished.emit(traj)
