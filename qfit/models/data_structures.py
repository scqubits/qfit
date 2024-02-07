from abc import ABC, abstractmethod, abstractproperty
from typing import List, Tuple, Union, Dict, Any, Optional

import numpy as np
from scqubits.core.storage import SpectrumData
import warnings

from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

from datetime import datetime

from qfit.models.parameter_settings import ParameterType
from qfit.widgets.grouped_sliders import SLIDER_RANGE

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem
ParentType = Union[QuantumSystem, HilbertSpace]


class Status:
    """
    Store the status of the application.
    """

    def __init__(
        self,
        statusSource: str,
        statusType: str,
        message: str,
        mse: Optional[float] = None,
        messageTime: Optional[float] = None,
    ):
        self.statusSource: str = statusSource
        self.statusType: str = statusType
        self.message: str = message
        self.mse: Union[float, None] = mse
        self.timestamp: datetime = datetime.now()
        self.messageTime: Optional[float] = messageTime

    def __str__(self):
        if self.statusType != "temp":
            return f"{self.timestamp} ({self.statusSource}) {self.statusType}, MSE: {self.mse} - {self.message}"
        else:
            return f"{self.timestamp} ({self.statusSource}) {self.statusType} lasting time {self.messageTime} s - {self.message}"

    def __repr__(self):
        return self.__str__()


class Tag:
    """
    Store a single dataset tag. The tag can be of different types:
    - NO_TAG: user did not tag data
    - DISPERSIVE_DRESSED: transition between two states tagged by
    dressed-states indices
    - DISPERSIVE_BARE: transition between two states tagged by
    bare-states indices

    Parameters
    ----------
    tagType: str
        one of the tag types listed above
    initial, final: int, or tuple of int, or None
        - For NO_TAG, no initial and final state are specified.
        - For DISPERSIVE_DRESSED, initial and final state are specified
        by an int dressed index.
        - FOR DISPERSIVE_BARE, initial and final state are specified by
        a tuple of ints (exc. levels of each subsys)
    photons: int or None
        - For NO_TAG, no photon number is specified.
        - For all other tag types, this int specifies the photon number rank of the transition.
    """

    def __init__(
        self,
        tagType: str = "NO_TAG",
        initial: Optional[Union[Tuple[int, ...], int]] = None,
        final: Optional[Union[Tuple[int, ...], int]] = None,
        photons: Optional[int] = None,
    ):
        self.tagType = tagType
        self.initial = initial
        self.final = final
        self.photons = photons

    def __str__(self):
        return "Tag: {0} {1} {2} {3}".format(
            self.tagType,
            str(self.initial),
            str(self.final),
            str(self.photons),
        )

    def __repr__(self):
        return self.__str__()


# ######################################################################
class PlotElement:
    """
    A data structure for passing and plotting elements on the canvas. 
    """
    name: str
    artists: Union[None, Artist, List[Artist]] = None
    _visible: bool = True

    def __init__(self, name: str) -> None:
        self.name = name

    def get_visible(self) -> bool:
        return self._visible

    def set_visible(self, value: bool) -> None:
        self._visible = value

        if self.artists is None:
            return

        if isinstance(self.artists, list):
            for artist in self.artists:
                artist.set_visible(value)
        else:
            self.artists.set_visible(value)

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        self.remove()

    @staticmethod
    def _remove_artist(artist: Artist) -> None:
        """
        Remove a single artist from the canvas
        """
        try:
            artist.remove()
        except ValueError:
            pass

    def remove(self) -> None:
        """
        Remove the element from the canvas
        """
        if self.artists is None:
            return

        if isinstance(self.artists, list):
            for artist in self.artists:
                self._remove_artist(artist)
        else:
            self._remove_artist(self.artists)

        self.artists = None

    def inheritProperties(self, element: "PlotElement") -> None:
        """
        Inherit the properties of another element. It usually happens when
        an element is updated by another, while we want to keep a ``global''
        property like visibility.
        """
        self.set_visible(element.get_visible())


class ImageElement(PlotElement):
    """
    Data structure for passing and plotting images
    """

    artists: AxesImage

    def __init__(self, name: str, z: np.ndarray, **kwargs):
        self.name = name
        self.z = z
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        """
        Plot the image on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        combined_kwargs = {**self.kwargs, **kwargs}
        self.artists = axes.imshow(self.z, **combined_kwargs)
        self.set_visible(self._visible)

    @property
    def xLim(self) -> Tuple[float, float]:
        """
        Return the x limits of the image
        """
        return (0, self.z.shape[1])

    @property
    def yLim(self) -> Tuple[float, float]:
        """
        Return the y limits of the image
        """
        return (self.z.shape[0], 0)


class MeshgridElement(PlotElement):
    """
    Data structure for passing and plotting meshgrids
    """

    artists: QuadMesh

    def __init__(
        self, name: str, x: np.ndarray, y: np.ndarray, z: np.ndarray, **kwargs
    ):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        """
        Plot the meshgrid on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        combined_kwargs = {**self.kwargs, **kwargs}
        self.artists = axes.pcolormesh(self.x, self.y, self.z, **combined_kwargs)
        self.set_visible(self._visible)

    @property
    def xLim(self) -> Tuple[float, float]:
        """
        Return the x limits of the meshgrid
        """
        return (np.min(self.x), np.max(self.x))

    @property
    def yLim(self) -> Tuple[float, float]:
        """
        Return the y limits of the meshgrid
        """
        return (np.min(self.y), np.max(self.y))


class ScatterElement(PlotElement):
    """
    Data structure for passing and plotting lines
    """

    artists: PathCollection

    def __init__(self, name: str, x: np.ndarray, y: np.ndarray, **kwargs):
        self.name = name
        self.x = x
        self.y = y
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        """
        Plot the scatter on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        combined_kwargs = {**self.kwargs, **kwargs}
        self.artists = axes.scatter(self.x, self.y, **combined_kwargs)
        self.set_visible(self._visible)


class SpectrumElement(PlotElement):
    """
    Data structure for passing and plotting spectra from scqubits
    """

    artists: List[Line2D]

    def __init__(
        self,
        name: str,
        overall_specdata: SpectrumData,
        highlighted_specdata: SpectrumData,
    ):
        self.name = name
        self.overall_specdata = overall_specdata
        self.highlighted_specdata = highlighted_specdata

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        """
        Plot the spectrum on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        fig = axes.get_figure()

        # since the scqubits backend do not return the artists, we need to
        # obtain the new artists by comparing the old and new artists
        artist_before = set(axes.get_children())

        self.overall_specdata.plot_evals_vs_paramvals(
            color="black",
            linewidth=2,
            linestyle="--",
            alpha=0.3,
            fig_ax=(fig, axes),
            **kwargs,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.highlighted_specdata.plot_evals_vs_paramvals(
                label_list=self.highlighted_specdata.labels,
                linewidth=2,
                fig_ax=(fig, axes),
                **kwargs,
            )

        artist_after = set(axes.get_children())
        self.artists = list(artist_after - artist_before)
        self.set_visible(self._visible)


class VLineElement(PlotElement):
    """
    Data structure for passing and plotting vertical lines
    """

    artists: List[Line2D]

    def __init__(self, name: str, x: Union[List[float], np.ndarray], **kwargs):
        self.name = name
        self.x = x
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes, **kwargs) -> None:
        """
        Plot the vertical line on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        combined_kwargs = {**self.kwargs, **kwargs}

        artists = []
        for x in self.x:
            artists.append(axes.axvline(x, **combined_kwargs))
        self.artists = artists
        self.set_visible(self._visible)


# Parameters ===========================================================
class ParamBase(ABC):
    intergerParameterTypes = ["cutoff", "truncated_dim"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        paramType: ParameterType,
    ):
        self.name = name
        self.parent = parent
        self.paramType = paramType

    def setParameterForParent(self):
        """
        Set the parameter for the parent
        """
        if isinstance(self.parent, HilbertSpace):
            assert self.paramType == "interaction_strength"
            interaction_index = int(self.name[1:]) - 1
            interaction = self.parent.interaction_list[interaction_index]
            interaction.g_strength = self.value
        else:
            setattr(self.parent, self.name, self.value)

    def _toInt(self, value: Union[int, float]) -> Union[int, float]:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return np.round(value).astype(int)
        else:
            return value

    @abstractproperty
    def value(self):
        """
        Get the value of the parameter
        """
        pass

    @value.setter
    def value(self, value):
        """
        Set the value of the parameter
        """
        pass


class DispParamBase(ParamBase):
    min: float

    def _toIntString(self, value: Union[int, float], precision=4) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return f"{value:.0f}"
        else:
            return f"{value:.{precision}f}".rstrip("0").rstrip(".")


class QMSweepParam(ParamBase):
    """
    A class for quantum model parameters that will be swept in experiments. 
    For example, ng and flux parameters in qubits. It stores a calibration_function
    for map the parameter value to the actual value (voltage) used in the experiment.

    Parameters
    ----------
    name: str
        The name of the parameter
    parent: Union[QuantumSystem, HilbertSpace]
        The parent of the parameter
    value: Union[float, int]
        The value of the parameter
    param_type: ParameterType
        The type of the parameter
    """

    attrToRegister = ["value"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        value: Union[float, int],
        param_type: ParameterType,
    ):
        super().__init__(name=name, parent=parent, paramType=param_type)

        self._value = value
        self.calibration_func = None

    def setCalibrationFunc(self, func):
        """
        Set the calibration function for the parameter
        """
        self.calibration_func = func

    @property
    def value(self) -> Union[int, float]:
        """
        Get the value of the parameter
        """
        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter. Will update the both the parameter stored and the
        parent object.
        """
        self._value = self._toInt(value)


class QMSliderParam(DispParamBase):
    """
    A class for parameters that are adjusted by a slider. 

    Parameters
    ----------
    name: str
        Name of the parameter
    parent: Union[QuantumSystem, HilbertSpace]
        The parent object of the parameter
    min: Union[int, float]
        The minimum value of the parameter
    max: Union[int, float]
        The maximum value of the parameter
    param_type: Literal[
        "EC",
        "EJ",
        "EL",
        "E_osc",
        "l_osc",
        "ng",
        "flux",
        "cutoff",
        "interaction_strength",
        "truncated_dim",
    ]
        The type of the parameter
    """

    sliderValueCallback: Callable
    sliderValueSetter: Callable
    boxValueCallback: Callable
    boxValueSetter: Callable
    minCallback: Callable
    minSetter: Callable
    maxCallback: Callable
    maxSetter: Callable
    overallValueSetter: Callable

    attrToRegister = ["value", "min", "max"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        param_type: ParameterType,
        value: Union[int, float],
        min: Union[int, float],
        max: Union[int, float],
    ):
        super().__init__(name=name, parent=parent, paramType=param_type)

        # a very bad temporary solution, when the model and the controller 
        # are more separated, this should be changed to:
        # parameter object only stores the value, min, max, and the type 
        # of the parameter. The controller should be responsible for
        # synchronizing the value of the parameter and the UI.
        self._init_value = value
        self._init_min = min
        self._init_max = max

    def setupUICallbacks(
        self,
        sliderValueCallback,
        sliderValueSetter,
        boxValueCallback,
        boxValueSetter,
        minCallback,
        minSetter,
        maxCallback,
        maxSetter,
    ):
        self.sliderValueCallback = sliderValueCallback
        self.sliderValueSetter = sliderValueSetter
        self.boxValueCallback = boxValueCallback
        self.boxValueSetter = boxValueSetter
        self.minCallback = minCallback
        self.minSetter = minSetter
        self.maxCallback = maxCallback
        self.maxSetter = maxSetter

        # a very bad temporary solution, when the model and the controller
        # are more separated, this should be in the controller.
        # after connect everything, we should update the value of the UI
        self.min = self._init_min
        self.max = self._init_max
        self.value = self._init_value

    def _normalizeValue(self, value: Union[int, float]) -> int:
        """
        Normalize the value of the parameter to a value between 0 and SLIDER_RANGE.
        """
        normalizedValue = (value - self.min) / (self.max - self.min) * SLIDER_RANGE
        return np.round(normalizedValue).astype(int)

    def _denormalizeValue(self, value: int) -> Union[int, float]:
        """
        Denormalize the value of the parameter to a value between min and max.
        """
        denormalizedValue = self.min + value / SLIDER_RANGE * (self.max - self.min)

        return self._toInt(denormalizedValue)

    def sliderValueToBox(self, *args, **kwargs):
        """
        When the value of the slider is changed, update the value of the box
        """
        sliderValue = self.sliderValueCallback()

        denormalizedValue = self._denormalizeValue(sliderValue)

        self.boxValueSetter(self._toIntString(denormalizedValue))

    def boxValueToSlider(self, *args, **kwargs):
        """
        When the value of the box is changed, update the value of the slider
        """
        try:
            boxValue = float(self.boxValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        normalizedValue = self._normalizeValue(boxValue)

        self.sliderValueSetter(normalizedValue)

    def onBoxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the box, update the value of the box and make the
        value consistent with the parameter type.
        """
        try:
            boxValue = float(self.boxValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.boxValueSetter(self._toIntString(boxValue))

    @property
    def value(self) -> Union[int, float]:
        """
        Special note: Will raise a ValueError if user input is not a number. Should be
        taken care of by the UI/controller.
        """
        boxValue = float(
            self.boxValueCallback()
        )  # will raise a ValueError if user input is not a number

        return self._toInt(boxValue)

    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter. Will update both value of the UI and the controller.
        """
        value = self._toInt(value)

        self.boxValueSetter(self._toIntString(value))
        self.sliderValueSetter(self._normalizeValue(value))

    @property
    def min(self) -> Union[int, float]:
        """
        Get the minimum value of the parameter from the UI
        """
        boxValue = float(
            self.minCallback()
        )

        return self._toInt(boxValue)
    
    @min.setter
    def min(self, value: Union[int, float]):
        """
        Set the minimum value of the parameter in the UI
        """
        self.minSetter(self._toIntString(value))

    def onMinEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the min box, update the value of the box and make the
        value consistent with the parameter type. 
        Besides, adjust the slider position.
        """
        try:
            boxValue = float(self.minCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.minSetter(self._toIntString(boxValue))
        self.boxValueToSlider()

    @property
    def max(self) -> Union[int, float]:
        """
        Get the maximum value of the parameter from the UI
        """
        boxValue = float(
            self.maxCallback()
        )

        return self._toInt(boxValue)
    
    @max.setter
    def max(self, value: Union[int, float]):
        """
        Set the maximum value of the parameter in the UI
        """
        self.maxSetter(self._toIntString(value))

    def onMaxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the max box, update the value of the box and make the
        value consistent with the parameter type. 
        Besides, adjust the slider position.
        """
        try:
            boxValue = float(self.maxCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.maxSetter(self._toIntString(boxValue))
        self.boxValueToSlider()

    # def initialize(self):
    #     # for test only
    #     self.value = (self.max + self.min) / 5 + self.min


class QMFitParam(DispParamBase):
    initValueCallback: Callable
    initValueSetter: Callable
    valueCallback: Callable
    valueSetter: Callable
    minCallback: Callable
    minSetter: Callable
    maxCallback: Callable
    maxSetter: Callable
    fixCallback: Callable
    fixSetter: Callable

    attrToRegister = ["initValue", "value", "min", "max", "isFixed"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        param_type: ParameterType,
    ):
        super().__init__(name=name, parent=parent, paramType=param_type)
        self._initValue = None
        self._value = None

    def setupUICallbacks(
        self,
        initValueCallback,
        initValueSetter,
        valueCallback,
        valueSetter,
        minCallback,
        minSetter,
        maxCallback,
        maxSetter,
        fixCallback,
        fixSetter,
    ):
        self.initValueCallback = initValueCallback
        self.initValueSetter = initValueSetter
        self.valueCallback = valueCallback
        self.valueSetter = valueSetter
        self.minCallback = minCallback
        self.minSetter = minSetter
        self.maxCallback = maxCallback
        self.maxSetter = maxSetter
        self.fixCallback = fixCallback
        self.fixSetter = fixSetter

    @property
    def min(self) -> Union[int, float]:
        """
        Get the minimum value of the parameter from the UI
        """
        return float(
            self.minCallback()
        )  # will raise a ValueError if user input is not a number

    @min.setter
    def min(self, value: Union[int, float]):
        """
        Set the minimum value of the parameter in the UI
        """
        self.minSetter(self._toIntString(value))

    def onMinEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the min box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.minCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.min = boxValue

    @property
    def max(self) -> Union[int, float]:
        """
        Get the maximum value of the parameter from the UI
        """
        return float(
            self.maxCallback()
        )  # will raise a ValueError if user input is not a number

    @max.setter
    def max(self, value: Union[int, float]):
        """
        Set the maximum value of the parameter in the UI
        """
        self.maxSetter(self._toIntString(value))

    def onMaxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the max box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.maxCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.max = boxValue

    @property
    def initValue(self) -> Union[int, float]:
        """
        Get the initial value of the parameter from the UI
        """
        if self._initValue is None:
            # self._initValue = float(self.initValueCallback())
            raise ValueError("Initial value of fitting parameter is not set yet.")

        return self._initValue

    @initValue.setter
    def initValue(self, value: Union[int, float]):
        """
        Set the initial value of the parameter in the UI
        """
        self._initValue = value
        self.initValueSetter(self._toIntString(value))

    def onInitValueEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the value box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.initValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.initValue = boxValue

    @property
    def value(self) -> Union[int, float]:
        """
        Get the value of the parameter from the UI
        """
        if self._value is None:
            # self._value = float(self.valueCallback())
            raise ValueError("Initial value of fitting parameter is not set yet.")

        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter in the UI
        """
        self._value = value
        self.valueSetter(self._toIntString(value))

    @property
    def isFixed(self) -> bool:
        """
        Check if the parameter is fixed
        """
        return self.fixCallback()

    @isFixed.setter
    def isFixed(self, value: bool):
        """
        Set the parameter to be fixed or not
        """
        self.fixSetter(value)

    def initialize(self):
        # for test only
        self.min = 0
        self.max = 1
        self.initValue = self.min
        self.value = self.initValue
        self.isFixed = False

    def valueToInitial(self):
        """
        Set the value of the parameter to the initial value
        """
        self.value = self.initValue
