from typing import Union, Dict, Optional
import numpy as np
from PySide6.QtCore import Signal, Slot
from qfit.models.parameter_set import (
    ParamSet, HSParamSet,
    ParamModelMixin,
)
from qfit.models.data_structures import ParamAttr, SliderParam, FitParam
from qfit.models.parameter_settings import DEFAULT_PARAM_MINMAX
from scqubits.core.hilbert_space import HilbertSpace

from qfit.models.registry import RegistryEntry


class SliderModelMixin(ParamModelMixin[SliderParam]):
    """
    Mixin class for the parameters that are connected to sliders, value text 
    boxes and min/max text boxes. 
    """

    updateSlider = Signal(ParamAttr)

    def _emitUpdateSlider(
        self,
        paramSet: ParamSet[SliderParam],
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
    ):
        """
        Emit updateSlider signal.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set.
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        """
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
        """
        Store the data from the view (slider or text box) and emit the signal
        to update its counterparts if necessary.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set.
        paramAttr: ParamAttr
            The parameter attribute.
        fromSlider: bool
            If the data comes from the slider.
        """
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


class PrefitHSParams(
    HSParamSet[SliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    """
    The model for the HilbertSpace parameters in the prefit stage. Those
    parameters are connected to sliders, value text boxes and min/max text
    boxes.

    Parameters
    ----------
    parent: QObject 
        The parent object.
    """
    attrs = SliderParam.dataAttr

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self, parent):
        # ordering matters here
        HSParamSet.__init__(self, SliderParam)
        SliderModelMixin.__init__(self, parent)

    def emitUpdateBox(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
        attr: Union[str, None] = None
    ):
        """
        Emit updateBox signal.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        attr: str
            The attribute to be updated.
        """
        self._emitUpdateBox(self, parentName=parentName, paramName=paramName, attr=attr)

    def emitUpdateSlider(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None
    ):
        """
        Emit updateSlider signal.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        """
        self._emitUpdateSlider(self, parentName=parentName, paramName=paramName)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Set the parameter from the other part of the backend, and then
        emit the signal to update the view.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        name: str
            The name of the parameter.
        attr: str
            The attribute to be updated.
        value: int | float
            The value to be set.
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

        Parameters
        ----------
        paramAttr: ParamAttr
            The parameter attribute.
        fromSlider: bool
            If the data comes from the slider.
        """
        super()._storeParamAttr(self, paramAttr, fromSlider=fromSlider)

    def registerAll(self) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters.

        Returns
        -------
        Dict[str, RegistryEntry]
            The registry entries.
        """
        return self._registerAll(self)

    # HilbertSpace related methods, could be a mixin class =============
    hilbertSpaceUpdated = Signal(HilbertSpace)

    # Signals 
    def emitHSUpdated(self):
        """
        In the prefit stage, send the updated HilbertSpace to the numerical
        model when updated.
        """
        self.hilbertSpaceUpdated.emit(self.hilbertspace)
        
    # Slots 
    @Slot(str, str)
    def updateParamForHS(
        self, 
        parentName: str | None = None, 
        paramName: str | None = None
    ):
        """
        Update the HilbertSpace when the parameters are updated.

        Parameters
        ----------
        parentName: str | None
            The name of the parent parameter.
        paramName: str | None
            The name of the parameter.
        """
        super().updateParamForHS(parentName, paramName)
        self.emitHSUpdated()

    # general model methods ============================================
    def toFitParams(self, scale: float = 0.15) -> ParamSet[FitParam]:
        """
        Prepare for the data transfer from the prefit parameters to the 
        fitting parameters.

        Parameters
        ----------
        scale: float
            The scale factor that determines the range of the fitting
            parameters.

        Returns
        -------
        ParamSet[FitParam]
            The fitting parameters.
        """
        paramSet = ParamSet[FitParam](FitParam)
        for parentName, parent in self.items():
            for paramName, param in parent.items():
                value = param.value

                # determine the min and max for fitting: the larger one 
                # between 20% of the default range and 40% of the 
                # current value
                defaultRange = DEFAULT_PARAM_MINMAX[param.paramType]
                range1 = (defaultRange["max"] - defaultRange["max"]) * scale / 2
                range2 = np.abs(value) * scale
                valRange = np.max([range1, range2])

                fitParam = FitParam(
                    name = paramName,
                    parent = param.parent,
                    paramType = param.paramType,
                    value = 0,  # not used
                    min = value - valRange/2,
                    max = value + valRange/2,
                    initValue = value,
                    isFixed = False,
                )
                paramSet.insertParam(parentName, paramName, fitParam)

        return paramSet


class PrefitCaliParams(
    ParamSet[SliderParam],
    SliderModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    """
    The model for the calibration parameters in the prefit stage. Those
    parameters are connected to sliders, value text boxes and min/max text
    boxes.

    Parameters
    ----------
    parent: QObject
        The parent object.
    """
    attrs = SliderParam.dataAttr

    updateSlider = Signal(ParamAttr)

    # mixin methods ====================================================
    def __init__(self, parent):
        # ordering matters here
        ParamSet.__init__(self, SliderParam)
        SliderModelMixin.__init__(self, parent)

    def emitUpdateBox(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
        attr: Union[str, None] = None
    ):
        """
        Emit updateBox signal.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        """
        self._emitUpdateBox(self, parentName=parentName, paramName=paramName, attr=attr)

    def emitUpdateSlider(
        self, 
        parentName: Union[str, None] = None, 
        paramName: Union[str, None] = None, 
    ):
        """
        Emit updateSlider signal.
        
        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        """
        self._emitUpdateSlider(self, parentName=parentName, paramName=paramName)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Set the parameter, emit the signal to update the view.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        name: str
            The name of the parameter.
        attr: str
            The attribute to be updated.
        value: int | float
            The value to be set.
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
        Store the data from the view.

        Parameters
        ----------
        paramAttr: ParamAttr
            The parameter attribute.
        fromSlider: bool
            If the data comes from the slider.
        """
        super()._storeParamAttr(self, paramAttr, fromSlider=fromSlider)

    def registerAll(self) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters.
        
        Returns
        -------
        Dict[str, RegistryEntry]
            The registry entries.
        """
        return self._registerAll(self)

    # Cailibration related methods =====================================
    updateCaliModel = Signal(ParamAttr)

    def replaceAllParam(
        self, 
        paramFromCaliModel: "ParamSet",
    ):
        """
        Replace all the parameters with the ones from the calibration model.
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
        """
        Send the calibration model the updated parameters so that the
        calibration function can be updated while prefitting.

        Parameters
        ----------
        parentName: str
            The name of the parent parameter.
        paramName: str
            The name of the parameter.
        """
        self.updateCaliModel.emit(ParamAttr(
            parentName,
            paramName,
            "value", 
            self[parentName][paramName].value
        ))
