from typing import Union
from PySide6.QtCore import Signal, Slot
from qfit.models.quantum_model_parameters import (
    HSParamSet, ParamSet,
    SliderModelMixin
)
from qfit.models.data_structures import ParamAttr, QMSliderParam
from scqubits.core.hilbert_space import HilbertSpace


class CombinedMeta(type(SliderModelMixin), type(ParamSet)):
    pass


class PrefitParamModel(
    HSParamSet[QMSliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = QMSliderParam.attrToRegister

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        HSParamSet.__init__(self, QMSliderParam)
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


class PrefitCaliModel(
    ParamSet[QMSliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    attrs = QMSliderParam.attrToRegister

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self):
        # ordering matters here
        ParamSet.__init__(self, QMSliderParam)
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
    caliParamUpdated = Signal(ParamAttr)

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
    def updateCalibration(
        self,
        parentName: str,
        paramName: str,
    ):
        paramAttr = self[parentName][paramName].exportAttr(attr="value")
        self.caliParamUpdated.emit(paramAttr)