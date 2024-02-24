from typing import Union, Dict, Optional
import numpy as np
from PySide6.QtCore import Signal, Slot
from qfit.models.parameter_set import (
    HSParamSet, ParamSet,
    ParamModelMixin,
)
from qfit.models.data_structures import ParamAttr, SliderParam, FitParam
from qfit.models.parameter_settings import DEFAULT_PARAM_MINMAX
from scqubits.core.hilbert_space import HilbertSpace

from qfit.models.registry import RegistryEntry



class SliderModelMixin(ParamModelMixin[SliderParam]):
    updateSlider = Signal(ParamAttr)

    def _emitUpdateSlider(
        self,
        paramSet: ParamSet[SliderParam],
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
    ):
        self._emitAttrByName(
            paramSet,
            self.updateSlider,
            parentName=parentName,
            paramName=paramName,
            attr="value",
            toSlider=True,
        )

    @Slot(ParamAttr)
    def _storeParamAttr(
        self,
        paramSet: ParamSet[SliderParam],
        paramAttr: ParamAttr,
        fromSlider: bool = False,
    ):
        super()._storeParamAttr(paramSet, paramAttr, fromSlider=fromSlider)

        if paramAttr.attr == "value":
            if fromSlider:
                self._emitUpdateBox(
                    paramSet, paramAttr.parentName, paramAttr.name, paramAttr.attr
                )
            elif not fromSlider:
                self._emitUpdateSlider(paramSet, paramAttr.parentName, paramAttr.name)
        elif paramAttr.attr in ["min", "max"]:
            self._emitUpdateSlider(paramSet, paramAttr.parentName, paramAttr.name)


class CombinedMeta(type(SliderModelMixin), type(ParamSet)):
    pass


class PrefitParamModel(
    HSParamSet[SliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = SliderParam.attrToRegister

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        HSParamSet.__init__(self, SliderParam)
        SliderModelMixin.__init__(self)

    def emitUpdateBox(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
        attr: Union[str, None] = None
    ):
        self._emitUpdateBox(self, parentName=parentName, paramName=paramName, attr=attr)

    def emitUpdateSlider(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None
    ):
        self._emitUpdateSlider(self, parentName=parentName, paramName=paramName)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Set the parameter, emit the signal to update the box and sliders.
        """
        super().setParameter(parentName, name, attr, value)

        self.emitUpdateBox(parentName, name, attr)
        self.emitUpdateSlider(parentName, name)

    @Slot()
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        fromSlider: bool = False,
    ):
        """
        Store the data from the view
        """
        super()._storeParamAttr(self, paramAttr, fromSlider=fromSlider)

    def registerAll(self) -> Dict[str, RegistryEntry]:
        return self._registerAll(self)

    # HilbertSpace related methods, could be a mixin class =============
    hilbertSpaceUpdated = Signal(HilbertSpace)

    # Signals 
    def emitHSUpdated(self):
        self.hilbertSpaceUpdated.emit(self.hilbertspace)
        
    # Slots 
    @Slot(str, str)
    def updateParent(
        self,
        parentName: str,
        paramName: str,
    ):
        param = self[parentName][paramName]
        param.setParameterForParent()
        self.emitHSUpdated()

    # general model methods ============================================
    def toFitParams(self) -> ParamSet[FitParam]:
        paramSet = ParamSet[FitParam](FitParam)
        for parentName, parent in self.items():
            for paramName, param in parent.items():
                value = param.value

                # determine the min and max for fitting: the larger one 
                # between 20% of the default range and 40% of the 
                # current value
                defaultRange = DEFAULT_PARAM_MINMAX[param.paramType]
                range1 = (defaultRange["max"] - defaultRange["max"]) * 0.2
                range2 = np.abs(value) * 0.4
                valRange = np.max([range1, range2])

                fitParam = FitParam(
                    name = paramName,
                    parent = param.parent,
                    paramType = param.paramType,
                    value = value,
                    min = value - valRange/2,
                    max = value + valRange/2,
                    initValue = value,
                    isFixed = False,
                )
                paramSet.insertParam(parentName, paramName, fitParam)

        return paramSet


class PrefitCaliModel(
    ParamSet[SliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = SliderParam.attrToRegister

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        ParamSet.__init__(self, SliderParam)
        SliderModelMixin.__init__(self)

    def emitUpdateBox(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
        attr: Union[str, None] = None
    ):
        self._emitUpdateBox(self, parentName=parentName, paramName=paramName, attr=attr)

    def emitUpdateSlider(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
    ):
        self._emitUpdateSlider(self, parentName=parentName, paramName=paramName)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Set the parameter, emit the signal to update the box and sliders.
        """
        super().setParameter(parentName, name, attr, value)

        self.emitUpdateBox(parentName, name, attr)
        self.emitUpdateSlider(parentName, name)

    @Slot()
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        fromSlider: bool = False,
    ):
        """
        Store the data from the view
        """
        super()._storeParamAttr(self, paramAttr, fromSlider=fromSlider)

    # Cailibration related methods =====================================
    updateCaliModel = Signal(ParamAttr)

    def replaceAllParam(
        self, 
        paramFromCaliModel: "ParamSet",
    ):
        """
        Used for put all the parameters from the calibration model to the prefit
        model.
        """
        self.parameters = paramFromCaliModel.parameters
        self.emitUpdateBox()
        self.emitUpdateSlider()

    @Slot(str, str)
    def emitUpdateCaliModel(
        self,
        parentName: str,
        paramName: str,
    ):
        # send the calibration model the updated parameters
        self.updateCaliModel.emit(ParamAttr(
            parentName,
            paramName,
            "value", 
            self[parentName][paramName].value
        ))

    # general model methods ============================================
    def toFitParams(self) -> ParamSet[FitParam]:
        paramSet = ParamSet[FitParam](FitParam)
        for parentName, parent in self.items():
            for paramName, param in parent.items():
                value = param.value

                fitParam = FitParam(
                    name = paramName,
                    parent = param.parent,
                    paramType = param.paramType,
                    value = value,
                    min = param.min,
                    max = param.max,
                    initValue = value,
                    isFixed = False,
                )
                paramSet.insertParam(parentName, paramName, fitParam)

        return paramSet
    