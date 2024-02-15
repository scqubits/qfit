from abc import ABC, ABCMeta, abstractmethod, abstractproperty
from typing import List, Tuple, Union, Dict, Any, Optional, overload, Literal

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


# Status ===============================================================
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

# Extracted Data =======================================================
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
    @overload
    def __init__(
        self,
        tagType: Literal["NO_TAG"] = "NO_TAG",
        initial: None = None,
        final: None = None,
        photons: None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        tagType: Literal["DISPERSIVE_DRESSED"],
        initial: int,
        final: int,
        photons: Optional[int] = None,
    ):
        ...

    @overload
    def __init__(
        self,
        tagType: Literal["DISPERSIVE_BARE"],
        initial: Tuple[int, ...],
        final: Tuple[int, ...],
        photons: Optional[int] = None,
    ):
        ...

    def __init__(
        self,
        tagType: Literal["NO_TAG", "DISPERSIVE_DRESSED", "DISPERSIVE_BARE"] = "NO_TAG",
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
    

class ExtrTransition:
    """
    A class for storing a transition extracted from the spectrum.

    Attributes
    ----------
    name: str
        The name of the transition
    data: np.ndarray
        The transition data, shape (2, N), where N is the number of data points
    rawX: List[np.ndarray]
        The raw control voltages data, shape (N, n), where n is the dimention of control voltages
    tag: Tag
        The tag of the transition 
    """
    def __init__(
        self, 
        name: str = "",
        data: np.ndarray = np.empty(shape=(2, 0), dtype=np.float_),   
        rawX: List[np.ndarray] = [],
        tag: Tag = Tag(),
    ) -> None:
        self.name = name
        self.data = data 
        self.rawX = rawX 
        self.tag = tag

    def count(self) -> int:
        return self.data.shape[1]
    
    def appendSorted(self, data: np.ndarray, rawX: np.ndarray):
        """
        It always keeps the data sorted by the x value.
        """
        if self.count() == 0:
            self.data = np.insert(self.data, 0, data, axis=1)
            self.rawX.append(rawX)
            return

        idx = np.searchsorted(self.data[0], data[0])
        self.data = np.insert(self.data, idx, data, axis=1)
        self.rawX.insert(idx, rawX)

    def remove(self, index: int):
        self.data = np.delete(self.data, index, axis=1)
        self.rawX.pop(index)

    def swapXY(self):
        """
        It happens only when rawX has shape (N, 1), where there is a chance
        for confusion between x and y.
        """
        if len(self.rawX) > 0:
            if self.rawX[0].shape[0] != 1:
                raise ValueError(
                    "The rawX data has more than one dimension, "
                    "meaning that there should be no chance for confusion."
                    "X and Y should be already distinguished."
                )

        self.data = self.data[[1, 0], :]
        self.rawX = list(self.data[0, :])
        

class ExtrSpectra(list[ExtrTransition]):
    """
    A bunch of transitions extracted from the same parameter sweep.
    """
    def __init__(
        self,
        *args: ExtrTransition,
    ) -> None:
        super().__init__(*args)

    def count(self) -> int:
        return sum([transition.count() for transition in self])

    def isEmpty(self) -> bool:
        for transition in self:
            if transition.count() > 0:
                return False
        return True

    def allNames(self) -> List[str]:
        return [transition.name for transition in self]
    
    def allData(self) -> List[np.ndarray]:
        """
        Return all data sorted by the transition name. 
        """
        return [transition.data for transition in self]
        
    def allDataConcated(self) -> np.ndarray:
        """
        Return all data concated
        """
        return np.concatenate(self.allData(), axis=1)
    
    def allRawX(self) -> List[List[np.ndarray]]:
        return [transition.rawX for transition in self]
    
    def allRawXConcated(self) -> List[np.ndarray]:
        return [rawX for rawXList in self.allRawX() for rawX in rawXList]
            
    def distinctSortedX(self) -> np.ndarray:
        """
        Return the distinct sorted x values of all transitions
        """
        allX = self.allDataConcated()[0]
        return np.sort(np.unique(allX))
    
    def swapXY(self):
        for transition in self:
            transition.swapXY()

    def rawXByX(self, x: float) -> np.ndarray:
        """
        Return the rawX data corresponding to the x value. Their relationship
        is linear. 
        """
        allData = self.allDataConcated()
        allRawX = self.allRawXConcated()

        if self.count() < 2:
            # try to find the exact x value
            for idx, x_ in enumerate(allData[0]):
                if x_ == x:
                    return allRawX[idx]
            raise ValueError("No data found for the x value")
            
        # calculate a linear mapping between the x values and the rawX data
        x1, x2 = allData[0, 0], allData[0, -1]
        rawX1, rawX2 = allRawX[0], allRawX[-1]

        return rawX1 + (rawX2 - rawX1) / (x2 - x1) * (x - x1)


class FullExtr(dict[str, ExtrSpectra]):
    """
    A class for storing all the extracted data from the experiment. 
    """

    def __init__(
        self,
        **kwargs: ExtrSpectra,
    ) -> None:
        super().__init__(**kwargs)

    def count(self) -> int:
        return sum([spectra.count() for spectra in self.values()])

    def swapXY(self):
        for value in self.values():
            value.swapXY()


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
class ParamAttr:
    """
    Raw data structure for passing parameter attributes from the View
    directly. Note that the value may be raw and needed to be converted
    to the proper type before being used.
    """
    def __init__(
        self,
        parantName: str,
        name: str,
        attr: str,
        value: Any,
    ):
        self.parantName = parantName
        self.name = name
        self.attr = attr
        self.value = value

    def __repr__(self) -> str:
        return f"{self.parantName}.{self.name}.{self.attr}: {self.value}"

    def __str__(self) -> str:
        return self.__repr__()
    

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

    def _toIntAsNeeded(self, value: Union[int, float]) -> Union[int, float]:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return np.round(value).astype(int)
        else:
            return value


class DispParamBase(ParamBase):
    attrToRegister: List[str]

    def _toIntString(self, value: Union[int, float], precision=4) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return f"{value:.0f}"
        else:
            return f"{value:.{precision}f}".rstrip("0").rstrip(".")
        
    def exportAttr(self, *args, **kwargs):
        pass

    def storeAttr(self, *args, **kwargs):
        pass

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
    paramType: ParameterType
        The type of the parameter
    """

    attrToRegister = ["value"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        value: Union[float, int],
        paramType: ParameterType,
    ):
        super().__init__(name=name, parent=parent, paramType=paramType)

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
        self._value = self._toIntAsNeeded(value)


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

    attrToRegister = ["value", "min", "max"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        paramType: ParameterType,
        value: Union[int, float],
        min: Union[int, float],
        max: Union[int, float],
    ):
        super().__init__(name=name, parent=parent, paramType=paramType)

        self.value: Union[int, float] = self._toIntAsNeeded(value)
        self.min: Union[int, float] = self._toIntAsNeeded(min)
        self.max: Union[int, float] = self._toIntAsNeeded(max)

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

        return self._toIntAsNeeded(denormalizedValue)
    
    # setters from UI ==================================================
    @overload
    def storeAttr(self, attr: str, value: str, fromSlider: Literal[False] = False) -> None:
        pass

    @overload
    def storeAttr(self, attr: str, value: int, fromSlider: Literal[True]) -> None:
        pass

    def storeAttr(self, attr: str, value: Union[str, int], fromSlider: bool = False):
        """
        Store the value of the parameter. If the source is a slider, the 
        value should be denormalized before being stored.
        """
        if fromSlider:
            value = self._denormalizeValue(value)
        else:
            value = self._toIntAsNeeded(float(value))

        setattr(self, attr, value)

    # getters for UI ===================================================
    @overload
    def exportAttr(self, attr: str, toSlider: Literal[False] = False) -> str:
        pass

    @overload
    def exportAttr(self, attr: str, toSlider: Literal[True]) -> int:
        pass

    def exportAttr(self, attr: str, toSlider: bool = False) -> Union[str, int]:
        """
        Export the value of the parameter. If the destination is a slider, the
        value should be normalized before being exported.
        """
        value = getattr(self, attr)
        if toSlider:
            return self._normalizeValue(value)
        else:
            return self._toIntString(value)


class QMFitParam(DispParamBase):

    attrToRegister = ["initValue", "value", "min", "max", "isFixed"]

    def __init__(
        self,
        name: str,
        parent: ParentType,
        paramType: ParameterType,
    ):
        super().__init__(name=name, parent=parent, paramType=paramType)

        # for test only
        self.min: Union[int, float] = 0
        self.max: Union[int, float] = 1
        self.initValue: Union[int, float] = self.min
        self.value: Union[int, float] = self.initValue
        self.isFixed: bool = False

    # setter for UI ====================================================
    def storeAttr(self, attr: str, value: Union[str, bool]):
        """
        Store the value of the parameter
        """
        if isinstance(value, str):
            value = self._toIntAsNeeded(float(value))

        setattr(self, attr, value)

    # getter for UI ====================================================
    def exportAttr(self, attr: str) -> Union[str, bool]: 
        """
        Export the value of the parameter
        """
        value = getattr(self, attr)
        if isinstance(value, bool):
            # should be put before the isinstance(value, int) condition
            # as bool is a subclass of int
            return value
        elif isinstance(value, int) or isinstance(value, float):
            return self._toIntString(value)
        else:
            raise ValueError(f"Unknown type of value: {value}")

    # ==================================================================
    def valueToInitial(self):
        """
        Set the value of the parameter to the initial value
        """
        self.value = self.initValue

