from abc import ABC, ABCMeta, abstractmethod, abstractproperty
from typing import List, Tuple, Union, Dict, Any, Optional, overload, Literal, Callable

import numpy as np
from scqubits.core.storage import SpectrumData
import warnings
from datetime import datetime
from copy import deepcopy

from cycler import cycler
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

import skimage.filters
import skimage.morphology
import skimage.restoration
from scipy.ndimage import gaussian_laplace
from matplotlib import colors as colors

from qfit.utils.helpers import (
    DictItem,
    OrderedDictMod,
    hasIdenticalCols,
    hasIdenticalRows,
    isValid1dArray,
    isValid2dArray,
)
from qfit.models.parameter_settings import ParameterType
from qfit.widgets.grouped_sliders import SLIDER_RANGE
from qfit.utils.helpers import OrderedDictMod
        

# Status ===============================================================
class Status:
    """
    Status of the fit, it is accepted by the StatusModel and displayed
    in the StatusBarView.

    Parameters
    ----------
    statusSource: Optional[str]
        The source of the status message
    statusType: str
        The type of the status message, e.g. "info", "warning", "error"
    message: Optional[str]
        The status message
    mse: Optional[float]
        The mean squared error in the prefit ot fit stage
    messageTime: Optional[float]
        The time the message is displayed
    """

    def __init__(
        self,
        statusSource: Optional[str],
        statusType: str,
        message: Optional[str] = None,
        mse: Optional[float] = None,
        messageTime: Optional[float] = None,
    ):
        self.statusSource: Optional[str] = statusSource
        self.statusType: str = statusType
        self.message: Optional[str] = message
        self.mse: Optional[float] = mse
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
    ): ...

    @overload
    def __init__(
        self,
        tagType: Literal["DISPERSIVE_DRESSED"],
        initial: int,
        final: int,
        photons: Optional[int] = None,
    ): ...

    @overload
    def __init__(
        self,
        tagType: Literal["DISPERSIVE_BARE"],
        initial: Tuple[int, ...],
        final: Tuple[int, ...],
        photons: Optional[int] = None,
    ): ...

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
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Tag):
            return False
        return (
            self.tagType == __value.tagType 
            and self.initial == __value.initial 
            and self.final == __value.final 
            and self.photons == __value.photons
        )
    
    def transitionStr(self) -> str:
        """
        Return the transition string
        """
        if self.tagType == "NO_TAG":
            return ""
        elif self.tagType == "DISPERSIVE_DRESSED":
            return f"{self.initial} - {self.final}"
        elif self.tagType == "DISPERSIVE_BARE":
            return f"{self.initial} - {self.final}"
        else:
            raise ValueError(f"Unknown tag type: {self.tagType}")


class ExtrTransition:
    """
    A class for storing a transition extracted from the spectrum.

    Attributes
    ----------
    name: str
        The name of the transition
    data: np.ndarray
        The transition data, shape (2, N), where N is the number of data points
    rawX: OrderedDictMod[str, np.ndarray]
        The raw x data, where the key is the name of the raw x data
    tag: Tag
        The tag of the transition
    """

    def __init__(
        self,
        name: str = "",
    ) -> None:
        self.name = name

        self._data: OrderedDictMod[str, np.ndarray] = OrderedDictMod()
        self.rawX: OrderedDictMod[str, np.ndarray] = OrderedDictMod()
        self.tag = Tag()

    @property
    def data(self) -> np.ndarray:
        """
        Return the transition data, shape (2, N), where N is the number of data points
        """
        if self.count() == 0:
            return np.empty((2, 0), dtype=float)
        return np.array(self._data.valList)

    def count(self) -> int:
        if len(self._data) == 0:
            return 0
        else:
            return len(self._data.valList[0])

    def append(
        self, data: OrderedDictMod[str, float], rawX: OrderedDictMod[str, float]
    ):
        """
        Append the a new data point to the transition. 
        It always keeps the data sorted by the x value.

        Parameters
        ----------
        data: OrderedDictMod[str, float]
            The data point to be appended, should have two elements: x & y,
            with the key being the name of the axis names
        rawX: OrderedDictMod[str, float]
            The raw x data point to be appended, where the key is the 
            name of the raw x data
        """
        if self.count() == 0:
            # the first data
            assert len(data) == 2, "The data should have two elements: x & y"
            for key, value in data.items():
                self._data[key] = np.array([value])
            for key, value in rawX.items():
                self.rawX[key] = np.array([value])
            return

        assert len(data) == 2, "The data should have two elements: x & y"
        assert len(rawX) == len(
            self.rawX
        ), "The rawX should have the same length as the existing rawX"

        for key, value in data.items():
            self._data[key] = np.append(self._data[key], value)
        for key, value in rawX.items():
            self.rawX[key] = np.append(self.rawX[key], value)

    def remove(self, index: int):
        """
        Remove the data point at the given index.

        Parameters
        ----------
        index: int
            The index of the data point to be removed
        """
        for key in self._data.keys():
            self._data[key] = np.delete(self._data[key], index)
        for key in self.rawX.keys():
            self.rawX[key] = np.delete(self.rawX[key], index)

    def swapXY(self):
        """
        It happens only when rawX has shape (N, 1), where there is a chance
        for confusion between x and y.
        """
        if self.count() > 0:
            if len(self.rawX.keys()) > 1:
                raise ValueError(
                    "The rawX data has more than one dimension, "
                    "meaning that there should be no chance for confusion."
                    "X and Y should be already distinguished."
                )

        # only when raw x only has one dimension
        self._data = OrderedDictMod(list(self._data.items())[::-1])
        self.rawX = OrderedDictMod(list(self._data.items())[0:1])  # raw x is x

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ExtrTransition):
            return False
        
        return (
            self.name == __value.name 
            and self._data == __value._data
            and self.rawX == __value.rawX
            and self.tag == __value.tag
        )


class ExtrSpectra(list[ExtrTransition]):
    """
    A bunch of transitions extracted from the same parameter sweep.

    Parameters
    ----------
    args: ExtrTransition
        The transitions to be stored in the spectra
    """

    def __init__(
        self,
        *args: ExtrTransition,
    ) -> None:
        super().__init__(args)

    def count(self) -> int:
        """
        Return the total number of data points in the spectra
        """
        return sum([transition.count() for transition in self])

    def isEmpty(self) -> bool:
        for transition in self:
            if transition.count() > 0:
                return False
        return True

    def allNames(self) -> List[str]:
        """
        All transition names
        """
        return [transition.name for transition in self]

    def allData(self) -> List[np.ndarray]:
        """
        All extracted data in a list
        """
        return [transition.data for transition in self]

    def allDataConcated(self) -> np.ndarray:
        """
        All extracted data concated
        """
        if self.count() == 0:
            return np.empty((2, 0), dtype=float)

        return np.concatenate(self.allData(), axis=1)

    def allRawXConcated(self) -> OrderedDictMod[str, np.ndarray]:
        """
        All raw x data concated
        """
        concatedRawX = deepcopy(self[0].rawX)

        for transition in self[1:]:
            for key, value in transition.rawX.items():
                concatedRawX[key] = np.concatenate([concatedRawX[key], value])

        return concatedRawX

    def distinctSortedX(self) -> np.ndarray:
        """
        Return the distinct sorted x values of all transitions
        """
        allX = self.allDataConcated()[0]
        return np.sort(np.unique(allX))

    def swapXY(self):
        for transition in self:
            transition.swapXY()


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

    Particularly, this class stores the artists on the canvas, enabling 
    the removal of the elements from the canvas. In method ``canvasPlot``,
    the artists are plotted on the canvas, and in method ``remove``, the
    artists are removed from the canvas.
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
        except ValueError as e:
            print(e)
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
        # axes.set_aspect('equal', adjustable='box')

        combined_kwargs = {
            "aspect": "auto",
            **self.kwargs, 
            **kwargs
        }
        self.artists = axes.imshow(self.z, **combined_kwargs)
        self.set_visible(self._visible)


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

            if self.highlighted_specdata.energy_table.size > 0:

                # reset the cycler so that the colors are consistent
                axes.set_prop_cycle(cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']))

                self.highlighted_specdata.plot_evals_vs_paramvals(
                    label_list=self.highlighted_specdata.labels,
                    linewidth=2,
                    fig_ax=(fig, axes),
                    **kwargs,
                )
            else:
                # no highlighted data (usually when evalsCount too small)
                pass

        axes.set_xlabel("")
        axes.set_ylabel("")

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
        parentName: str,
        name: str,
        attr: str,
        value: Any,
    ):
        self.parentName = parentName
        self.name = name
        self.attr = attr
        self.value = value

    def __repr__(self) -> str:
        return f"{self.parentName}.{self.name}.{self.attr}: {self.value}"

    def __str__(self) -> str:
        return self.__repr__()


class ParamBase(ABC):
    """
    The base class for any parameters in qfit. It stores the parameter name,
    parent name, parameter type, and value. It provides basic methods for 
    converting the value to an integer following the parameter type. It also
    provides the method for comparing two parameters based on dataAttr.

    Parameters
    ----------
    name: str
        The name of the parameter
    parent: str
        The parent of the parameter
    paramType: ParameterType
        The type of the parameter
    value: Union[int, float]
        The value of the parameter
    """
    dataAttr: List[str] = ["value"]
    intergerParameterTypes = ["cutoff", "truncated_dim"]

    def __init__(
        self,
        name: str,
        parent: str,
        paramType: ParameterType,
        value: Union[int, float],
    ):
        self.name = name
        self.parent = parent
        self.paramType = paramType
        self.value = self._toIntAsNeeded(value)

    def _toIntAsNeeded(self, value: Union[int, float]) -> Union[int, float]:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return np.round(value).astype(int)
        else:
            return value
        
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ParamBase):
            return False
        return all([
            getattr(self, attr) == getattr(__value, attr) 
            for attr in self.dataAttr
        ])

class DispParamBase(ParamBase):
    """
    A base class for parameters that are stored in a model connected to 
    views. It provides methods for exporting and storing the parameter value. 
    """
    def _toIntStrAsNeeded(self, value: Union[int, float], precision=4) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.paramType in self.intergerParameterTypes:
            return f"{value:.0f}"
        else:
            return f"{value:.{precision}f}".rstrip("0").rstrip(".")

    def exportAttr(self, *args, **kwargs) -> Any:
        pass

    def storeAttr(self, attr: str, value: Any, *args, **kwargs):
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
    parent: str
        The parent of the parameter
    value: Union[float, int]
        The value of the parameter
    paramType: ParameterType
        The type of the parameter
    """

    calibration_func: Callable[[Dict[str, float]], float]

    dataAttr = ["value"]

    def __init__(
        self,
        name: str,
        parent: str,
        value: Union[float, int],
        paramType: ParameterType,
    ):
        super().__init__(name=name, parent=parent, paramType=paramType, value=value)

    def setCalibrationFunc(self, func):
        """
        Set the calibration function for the parameter
        """
        self.calibration_func = func

    def setValueWithCali(self, value: Dict[str, float]):
        """
        Set the value of the parameter with the calibration function
        """
        self.value = self.calibration_func(value)


class SliderParam(DispParamBase):
    """
    A class for parameters that are adjusted by a slider (and a text box). 
    It has three dataAttr: value, min, and max. It provides methods for 
    exporting and storing the parameter value with the slider and the text box.

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
    param_type: ParameterType
        The type of the parameter
    """

    dataAttr = ["value", "min", "max"]

    def __init__(
        self,
        name: str,
        parent: str,
        paramType: ParameterType,
        value: Union[int, float],
        min: Union[int, float],
        max: Union[int, float],
    ):
        super().__init__(name=name, parent=parent, paramType=paramType, value=value)

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
    def storeAttr(self, attr: str, value: str, fromSlider: Literal[False]) -> None:
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
            convertedValue = self._denormalizeValue(value)
        else:
            convertedValue = self._toIntAsNeeded(float(value))

        setattr(self, attr, convertedValue)

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
            return self._toIntStrAsNeeded(value)


class FitParam(DispParamBase):
    """
    A class for parameters that are adjusted by a fit. It has five dataAttr:
    initValue, value, min, max, and isFixed. It provides methods for exporting
    and storing the parameter value with the fit.

    Parameters
    ----------
    name: str
        Name of the parameter
    parent: Union[QuantumSystem, HilbertSpace]
        The parent object of the parameter
    paramType: ParameterType
        The type of the parameter
    value: Union[int, float]
        The value of the parameter
    min: Union[int, float]
        The minimum value of the parameter
    max: Union[int, float]
        The maximum value of the parameter
    initValue: Union[int, float]
        The initial value of the parameter
    isFixed: bool
        Whether the parameter is fixed
    """
    
    dataAttr = ["initValue", "value", "min", "max", "isFixed"]

    def __init__(
        self,
        name: str,
        parent: str,
        paramType: ParameterType,
        value: Union[int, float] = 0,
        min: Union[int, float] = 0,
        max: Union[int, float] = 1,
        initValue: Union[int, float] = 0,
        isFixed: bool = False,
    ):
        super().__init__(name=name, parent=parent, paramType=paramType, value=value)
        self.min = self._toIntAsNeeded(min)
        self.max = self._toIntAsNeeded(max)
        self.initValue = self._toIntAsNeeded(initValue)
        self.isFixed = isFixed

    # setter for UI ====================================================
    def storeAttr(self, attr: str, value: Union[str, bool]):
        """
        Store the value of the parameter
        """
        if isinstance(value, str):
            convertedValue = self._toIntAsNeeded(float(value))
        else:
            convertedValue = value

        setattr(self, attr, convertedValue)

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
            return self._toIntStrAsNeeded(value)
        else:
            raise ValueError(f"Unknown type of value: {value}")

    # ==================================================================
    def valueToInitial(self):
        """
        Set the value of the parameter to the initial value
        """
        self.value = self.initValue


class CaliTableRowParam(DispParamBase):
    """
    The updated class for calibration table parameters. It has three dataAttr:
    value, sweepParamName, and parentSystemName. sweepParamName and parentSystemName
    are matched with the names in other parameters. It provides methods for exporting
    and storing the parameter value with the calibration table.

    Parameters
    ----------
    colName: str
        Name of the parameter
    rowIdx: str
        The row index of the parameter
    paramType: ParameterType
        The type of the parameter
    value: float
        The value of the parameter
    parentSystemName: str
        The name of the parent system
    sweepParamName: str
        The name of the sweep parameter
    value: float
        The value of the parameter
    """

    dataAttr = [
        "value",
        "sweepParamName",
        "parentSystemName",
    ]

    def __init__(
        self,
        colName: str,
        rowIdx: str,
        paramType: ParameterType,
        parentSystemName: str,
        sweepParamName: str,
        value: float,
    ):
        super().__init__(name=colName, parent=rowIdx, paramType=paramType, value=value)
        self.parentSystemName = parentSystemName
        self.sweepParamName = sweepParamName

    # setter for UI ====================================================
    def storeAttr(self, attr: str, value: Union[str, bool]):
        """
        Store the value of the parameter
        """
        if isinstance(value, str):
            convertedValue = self._toIntAsNeeded(float(value))

        setattr(self, attr, convertedValue)

    # getter for UI ====================================================
    def exportAttr(self, attr: str) -> Union[str, bool]:
        """
        Export the value of the parameter
        """
        value = getattr(self, attr)

        if isinstance(value, bool):
            return value
        elif isinstance(value, int) or isinstance(value, float):
            return self._toIntStrAsNeeded(value)
        elif isinstance(value, str):
            return value
        elif value is None:
            return ""
        else:
            raise ValueError(f"Unknown type of value: {value}")

# measurement data =====================================================
class MeasMetaInfo:
    def __init__(
        self,
        name: str,
        file: str,
        shape: Tuple[int, int],
        xCandidateNames: List[str],
        yCandidateNames: List[str],
        zCandidateNames: List[str],
        discardedKeys: List[str],

    ):
        self.name = name
        self.file = file
        self.shape = shape
        self.xCandidateNames = xCandidateNames
        self.yCandidateNames = yCandidateNames
        self.zCandidateNames = zCandidateNames
        self.discardedKeys = discardedKeys

    def __str__(self) -> str:
        return f"""
MeasMetaInfo: 
- Name: {self.name}
- File: {self.file}
- Data Shape: {self.shape}
- X Axes Candidates: {", ".join(self.xCandidateNames)}
- Y Axes Candidates: {", ".join(self.yCandidateNames)}
- Z Axes Candidates: {", ".join(self.zCandidateNames)}
- Incompatible Items: {", ".join(self.discardedKeys)}
"""

    def __repr__(self) -> str:
        return self.__str__()
    

class MeasRawXYConfig:
    def __init__(
        self,
        checkedX: List[str] = [],
        checkedY: List[str] = [],
        xCandidates: List[str] = [],
        yCandidates: List[str] = [],
        grayedX: List[str] = [],
        grayedY: List[str] = [],
        allowTranspose: bool = False,
        allowContinue: bool = False,
    ):
        self.xCandidates = sorted(xCandidates)
        self.yCandidates = sorted(yCandidates)
        self.checkedX = checkedX
        self.checkedY = checkedY
        self.grayedX = grayedX
        self.grayedY = grayedY
        self.allowTranspose = allowTranspose
        self.allowContinue = allowContinue

    def __str__(self) -> str:
        return f"""
MeasRawXYConfig:
- X Axes Candidates: {", ".join(self.xCandidates)}
- Y Axes Candidates: {", ".join(self.yCandidates)}
- Checked X Axes: {", ".join(self.checkedX)}
- Checked Y Axes: {", ".join(self.checkedY)}
- Grayed X Axes: {", ".join(self.grayedX)}
- Grayed Y Axes: {", ".join(self.grayedY)}
- Transpose Allowed: {self.allowTranspose}
- Continue Allowed: {self.allowContinue}
"""
    
    def __repr__(self) -> str:
        return self.__str__()
    

class FilterConfig:
    def __init__(
        self,
        topHat: bool,
        wavelet: bool,
        edge: bool,
        bgndX: bool,
        bgndY: bool,
        log: bool,
        min: float,
        max: float,
        color: str,
    ):
        self.topHat = topHat
        self.wavelet = wavelet
        self.edge = edge
        self.bgndX = bgndX
        self.bgndY = bgndY
        self.log = log
        self.min = min
        self.max = max
        self.color = color
    

class MeasurementData:
    """
    Base class for storing and manipulating measurement data. The primary 
    measurement data (zData) is expected to be a 2d or 3d float ndarray.

    Parameters
    ---------
    name: str
        name of the measurement data, usually the name of the file
    rawData: Any
        the raw data extracted from a data file

    Attributes
    ----------
    name: str
        name of the measurement data, usually the name of the file
    rawData: Any
        the raw data extracted from a data file
    _zCandidates: OrderedDictMod[str, ndarray]
        A dictionary of 2d ndarrays, which may be suitable as zData candidates
    rawX: OrderedDictMod[str, ndarray]
        A dictionary of 1d ndarrays, which has the same length. They are
        multiple tuning parameters.
    rawY: OrderedDictMod[str, ndarray]
        A dictionary of 1d ndarrays, which has the same length. We require
        that rawY has only one element, which is the frequency axis.        
    """

    # candidates: all possible x, y, and z data that are compatible in shape
    zCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 2d ndarrays
    xCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 1d ndarrays
    yCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 1d ndarrays
    discardedKeys: List[str] = []

    # raw data: the selected x, y, and z data, indicating the actual tuning
    # parameters and the measurement data
    _rawXNames: List[str] = []
    _rawYName: List[str] = []

    # principal data: the z data that are used to plot and the x, y data that
    # serves as coordinates in the plot
    _principalZ: DictItem
    _principalX: DictItem     # x axis that has the largest change
    _principalY: DictItem     

    # filters
    _bgndSubtractX = False
    _bgndSubtractY = False
    _topHatFilter = False
    _waveletFilter = False
    _edgeFilter = False
    _logColoring = False
    _zMin = 0.0
    _zMax = 100.0
    _colorMapStr = "PuOr"   # it's a property stored in each data, but won't 
                            # be used in generatePlotElement. It's used in
                            # the mpl canvas view to set the color map of the
                            # entire canvas.

    def __init__(self, figName: str, rawData, file: str):
        super().__init__()

        self.name: str = figName
        self.rawData = rawData
        self.file = file

    # properties =======================================================
    @property
    def principalZ(self) -> DictItem:
        """
        Return current dataset describing the z values (measurement data) with all filters etc. applied.

        Returns
        -------
        DataItem
        """
        zData = deepcopy(self._principalZ)

        if self._bgndSubtractX:
            zData.data = self._doBgndSubtraction(zData.data, axis=1)
        if self._bgndSubtractY:
            zData.data = self._doBgndSubtraction(zData.data, axis=0)
        if self._topHatFilter:
            zData.data = self._applyTopHatFilter(zData.data)
        if self._waveletFilter:
            zData.data = self._applyWaveletFilter(zData.data)
        if self._edgeFilter:
            zData.data = gaussian_laplace(zData.data, 1.0)

        zData.data = self._clip(zData.data)

        return zData

    @property
    def principalX(self) -> DictItem:
        """
        Return current dataset describing the x-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._principalX

    @property
    def principalY(self) -> DictItem:
        """
        Return current dataset describing the y-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._principalY
    
    @property
    def rawXNames(self) -> List[str]:
        return self._rawXNames

    @property
    def rawYNames(self) -> List[str]:
        return self._rawYName
    
    @property
    def rawX(self):
        return OrderedDictMod({
            key: value for key, value in self.xCandidates.items() 
            if key in self._rawXNames
        })
    
    @property
    def rawY(self):
        return OrderedDictMod({
            key: value for key, value in self.yCandidates.items()
            if key in self._rawYName
        })
    
    @property
    def ambiguousZOrient(self) -> bool:
        """
        Return True if the zData is ambiguous in orientation, even if specifying
        the x and y axes. This can happen if the zData has the same number of
        rows and columns.
        """
        return self.principalZ.data.shape[0] == self.principalZ.data.shape[1]
    
    # manipulation =====================================================
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MeasurementData):
            return False

        dataAttrs = [
            "name",
            "rawData",
            "_zCandidates",
            "xCandidates",
            "yCandidates",
            "_rawXNames",
            "_rawYName",
            "_principalZ",
            "_principalX",
            "_principalY",
            "_bgndSubtractX",
            "_bgndSubtractY",
            "_topHatFilter",
            "_waveletFilter",
            "_edgeFilter",
            "_logColoring",
            "_zMin",
            "_zMax",
        ]
        
        return all([
            getattr(self, attr) == getattr(__value, attr)
            for attr in dataAttrs]
        )
    
    def generateMetaInfo(self) -> MeasMetaInfo:
        """
        Generate the meta information of the measurement data
        """
        return MeasMetaInfo(
            name=self.name,
            file=self.file,
            shape=self.principalZ.data.shape[:2],
            xCandidateNames=self.xCandidates.keyList,
            yCandidateNames=self.yCandidates.keyList,
            zCandidateNames=self.zCandidates.keyList,
            discardedKeys=self.discardedKeys,
        )

    @abstractmethod
    def generatePlotElement(self) -> Union[ImageElement, MeshgridElement]:
        """
        Generate a plot element from the current data

        Returns
        -------
        PlotElement
        """
        pass

    def _transposeZ(self, array: np.ndarray) -> np.ndarray:
        """
        Transpose the zData array.
        """
        if array.ndim == 2:
            return array.transpose()
        elif array.ndim == 3:
            return array.transpose(1, 0, 2)
        else:
            raise ValueError("array must be 2D or 3D")
    
    def setRawXY(
        self, 
        xNames: List[str],
        yNames: List[str],
    ):
        """
        Given the names of the x axis candidates, set the raw x axis names and
        the principal x axis.
        """
        # check if the names are valid
        if not all([name in self.xCandidates.keyList for name in xNames]):
            raise ValueError("Invalid raw x axis names as not all are in "
                             "the x axis candidate list")
        if len(yNames) != 1:
            raise ValueError("Invalid raw y axis names as there must be "
                             "only one y axis")
        if yNames[0] not in self.yCandidates.keyList:
            raise ValueError("Invalid raw y axis name as it is not in the y "
                             "axis candidate list")
        if yNames[0] in xNames:
            raise ValueError("The raw x and y axis names must be different")

        self._rawXNames = xNames
        self._rawYName = yNames

        # reset the principal x axis
        self._resetPrincipalXY()

    def setPrincipalZ(self, item: int | str):
        """
        Set the principal z dataset by the index or the name of the data.
        """
        if isinstance(item, str):
            itemIndex = self.zCandidates.keyList.index(item)
        self._principalZ = self.zCandidates.itemByIndex(itemIndex)

    def _initRawXY(self):
        """
        Initialize the raw x and y axis by the first compatible x and y axis.
        """
        self._rawXNames = self.xCandidates.keyList[:1]
        self._rawYName = self.yCandidates.keyList[:1]

        # if rawX and rawY are the same, set rawY to the next compatible y axis.
        # It can always be done because there are pixel coordinates as the last 
        # resort
        if self._rawXNames == self._rawYName:
            self._rawYName = self.yCandidates.keyList[1:2]

    def _removePixelCoord(self):
        """
        Remove pixel coordinates from the x and y axis candidates. That is 
        needed when we need to swap XY and regenerate a new set of pixel
        coordinates.
        """
        self.xCandidates = OrderedDictMod({
            key: value for key, value in self.xCandidates.items()
            if not key.startswith("pixel_coord")
        })
        self.yCandidates = OrderedDictMod({
            key: value for key, value in self.yCandidates.items()
            if not key.startswith("pixel_coord")
        })
        
        # if the pixel coordinates are chosen to be the raw x and y axis,
        # reset the raw x and y axis
        reset = False
        for name in self._rawXNames:
            if name.startswith("pixel_coord"):
                reset = True
        for name in self._rawYName:
            if name.startswith("pixel_coord"):
                reset = True
        if reset:
            self._initRawXY()
            self._resetPrincipalXY()

    def _addPixelCoord(self):
        """
        Add pixel coordinates as the last resort for x and y axis candidates.
        """
        ydim, xdim = self._principalZ.data.shape
        self.xCandidates.update({"pixel_coord_x": np.arange(xdim)})
        self.yCandidates.update({"pixel_coord_y": np.arange(ydim)})
        
    def _resetPrincipalXY(self):
        """
        The principal x axis corresponds to the x axis that has the
        largest change in the data.
        Since there should only be one y axis, the principal y axis is
        the first y axis.
        """
        if len(self.rawX) > 1:
            idx = np.argmax(
                [
                    np.abs(data[-1] - data[0])
                    for data in self.rawX.values()
                ]
            )
            self._principalX = self.rawX.itemByIndex(int(idx))
        else:
            self._principalX = self.rawX.itemByIndex(0)

        self._principalY = self.rawY.itemByIndex(0)

    def swapXY(self):
        """
        Swap the x and y axes and transpose the zData array.
        """
        self._removePixelCoord()

        # if the user have already selected multiple x axes, we will only
        # keep the first one, as y axis is unique
        self._rawXNames = self._rawXNames[:1]

        swappedZCandidates = {
            key: self._transposeZ(array) for key, array in self.zCandidates.items()
        }
        self.zCandidates = OrderedDictMod(swappedZCandidates)
        self._principalZ.data = self._transposeZ(self._principalZ.data)

        self.xCandidates, self.yCandidates = self.yCandidates, self.xCandidates
        self._rawXNames, self._rawYName = self._rawYName, self._rawXNames

        self._addPixelCoord()
        self._resetPrincipalXY()
        
    def transposeZ(self):
        """
        Transpose the zData array without swapping the x and y axes. It should 
        be used when the zData array is ambiguous in orientation - when the
        number of rows and columns are the same.
        """
        if not self.ambiguousZOrient:
            raise ValueError("The zData array is not ambiguous in orientation")
        
        self.zCandidates = OrderedDictMod({
            key: self._transposeZ(array) for key, array in self.zCandidates.items()
        })
        self._principalZ.data = self._transposeZ(self._principalZ.data)

    def rawXByPrincipalX(self, principalX: float) -> OrderedDictMod[str, float]:
        """
        Return the raw x values corresponding to the current x values.

        Parameters
        ----------
        principalX: float
            the value of the principal x axis

        Returns
        -------
        OrderedDictMod[str, float]
        """
        fraction = (principalX - self.principalX.data[0]) / (
            self.principalX.data[-1] - self.principalX.data[0]
        )
        rawX = OrderedDictMod()
        for name, data in self.rawX.items():
            rawX[name] = data[0] + fraction * (data[-1] - data[0])
        return rawX

    # filters =============================================================
    def setFilter(self, config: FilterConfig):
        """
        Set the filter configuration
        """
        self._topHatFilter = config.topHat
        self._waveletFilter = config.wavelet
        self._edgeFilter = config.edge
        self._bgndSubtractX = config.bgndX
        self._bgndSubtractY = config.bgndY
        self._logColoring = config.log
        self._zMin = config.min
        self._zMax = config.max
        self._colorMapStr = config.color

    def getFilter(self) -> FilterConfig:
        """
        Get the filter configuration
        """
        return FilterConfig(
            topHat=self._topHatFilter,
            wavelet=self._waveletFilter,
            edge=self._edgeFilter,
            bgndX=self._bgndSubtractX,
            bgndY=self._bgndSubtractY,
            log=self._logColoring,
            min=self._zMin,
            max=self._zMax,
            color = self._colorMapStr,
        )

    def currentMinMax(self, array2D: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Return the clipped min max values of the current zData and the 
        unprocessed min max values.

        Returns
        -------
        Tuple[float, float, float, float]
            clipped minimum of the current zData by the range slider, 
            clipped maximum of the current zData by the range slider, 
            unprocessed minimum of the current zData, 
            unprocessed maximum of the current zData
        """
        if array2D.ndim != 2:
            raise ValueError("array must be 2D")
        
        normedMin = min(self._zMin, self._zMax) / 100
        normedMax = max(self._zMin, self._zMax) / 100

        rawZMin = array2D.min()
        rawZMax = array2D.max()
        # Choose Z value range according to the range slider values.
        zMin = rawZMin + normedMin * (rawZMax - rawZMin)
        zMax = rawZMin + normedMax * (rawZMax - rawZMin)

        return zMin, zMax, rawZMin, rawZMax

    def _doBgndSubtraction(self, array: np.ndarray, axis=0):
        """
        Subtract the background from the data and rescale the zData to the
        range of the original data.
        """
        previousMin = np.nanmin(array)
        previousMax = np.nanmax(array)
        previousRange = previousMax - previousMin

        # subtract the background
        background = np.nanmedian(array, axis=axis, keepdims=True)
        avgArray = array - background

        # rescale the data to the range of the original data
        currentMin = np.nanmin(avgArray)
        currentMax = np.nanmax(avgArray)
        currentRange = currentMax - currentMin
        if currentRange == 0:
            currentRange = previousRange = 1

        avgArray = (avgArray - currentMin) / currentRange * previousRange + previousMin

        if array.ndim == 3:
            avgArray = np.round(avgArray, 0).astype(int)

        return avgArray

    def _applyWaveletFilter(self, array: np.ndarray):
        """
        Apply the wavelet filter to the data.
        """
        return skimage.restoration.denoise_wavelet(array, rescale_sigma=True)
    
    def _applyEdgeFilter(self, array: np.ndarray):
        """
        Apply the edge filter to the data.
        """
        # Check if the data is a 3D array
        if len(array.shape) == 3:
            # Apply the filter to each color channel separately
            for i in range(array.shape[2]):
                array[:, :, i] = gaussian_laplace(array[:, :, i], 1.0)
        else:
            array = gaussian_laplace(array, 1.0)

        return array
    
    def _applyTopHatFilter(self, array: np.ndarray):
        """
        Apply the top hat filter to the data.
        """
        # Check if the array is 3D
        if len(array.shape) == 3:
            # Apply the filter to each color channel separately
            result = np.zeros_like(array)
            for i in range(array.shape[2]):
                result[:, :, i] = self._applyTopHatFilter(array[:, :, i])
            return result

        # Original function for 1D or 2D arrays
        array = array - np.mean(array)
        stdvar = np.std(array)

        histogram, bin_edges = np.histogram(
            array, bins=30, range=(-1.5 * stdvar, 1.5 * stdvar)
        )
        max_index = np.argmax(histogram)
        mid_value = (bin_edges[max_index + 1] + bin_edges[max_index]) / 2
        array = array - mid_value
        stdvar = np.std(array)
        ones = np.ones_like(array)

        return (
            np.select(
                [array > 1.5 * stdvar, array < -1.5 * stdvar, True],
                [ones, ones, 0.0 * ones],
            )
            * array
        )
    
    def _clip(self, array: np.ndarray):
        """
        Clip the data to the range of the slider and rescale the data to the
        range of the original data.
        """
        # check if the array is 3D
        if len(array.shape) == 3:
            # Apply the filter to each color channel separately
            result = np.zeros_like(array)
            for i in range(array.shape[2]):
                result[:, :, i] = self._clip(array[:, :, i])

            return np.round(result, 0).astype(int)
        
        # Original function for 1D or 2D arrays
        zMin, zMax, rawZMin, rawZMax = self.currentMinMax(array)

        # Clip the data to the range of the slider
        array = np.clip(array, zMin, zMax)

        # Rescale the data to the range of the original data
        array = (array - zMin) / (zMax - zMin) * (rawZMax - rawZMin) + rawZMin

        return array


class NumMeasData(MeasurementData):
    """
    Class for storing and manipulating measurement data. The primary 
    measurement data (zData) is expected to be a 2d float ndarray, and the
    x and y axis data are expected to be 1d float ndarrays.

    Parameters
    ---------
    rawData: list of ndarray
        list containing all 1d and 2d arrays (floats) extracted from a data file
    """

    def __init__(
        self,
        name: str,
        rawData: OrderedDictMod[str, np.ndarray],
        file: str,
    ):
        super().__init__(name, rawData, file)
        self._initXYZ()

    # properties =======================================================
    @property
    def discardedKeys(self) -> List[str]:
        """
        The keys that are discarded from the raw data
        """
        allKeys = self.rawData.keys()
        acceptedKeys = self.zCandidates.keyList + self.xCandidates.keyList + self.yCandidates.keyList
        return [
            key for key in allKeys
            if key not in acceptedKeys
        ]

    # initialization ===================================================
    @staticmethod
    def _findZCandidates(rawData: Union[OrderedDictMod, Dict]):
        """
        Find all 2d ndarrays in the rawData dict that are suitable as zData candidates. All of the zData candidates must have the same shape,
        as they reperseent the data for the same measurement, usually the 
        amplitude or phase of the signal.
        """
        zCandidates = OrderedDictMod()
        for name, theObject in rawData.items():
            if isinstance(theObject, np.ndarray) and isValid2dArray(theObject):
                if not (hasIdenticalCols(theObject) or hasIdenticalRows(theObject)):
                    zCandidates[name] = theObject

        # all zCandidates must have the same shape
        if len(set([z.shape for z in zCandidates.values()])) > 1:
            raise ValueError("zCandidates must have the same shape")
        
        # if there are no zCandidates, raise an error
        if not zCandidates:
            raise ValueError("No suitable zData candidates found")

        return zCandidates

    def _findXYCandidates(self):
        """
        By trying to match the dimensions of the zData with the x and y axis candidates,
        find the x and y axis candidates that are compatible with the zData.
        """
        # find xy candidates
        xyCandidates = OrderedDictMod()
        for name, theObject in self.rawData.items():
            if isinstance(theObject, np.ndarray):
                if isValid1dArray(theObject):
                    xyCandidates[name] = theObject.flatten()
                if isValid2dArray(theObject) and hasIdenticalRows(theObject):
                    xyCandidates[name] = theObject[0]
                if isValid2dArray(theObject) and hasIdenticalCols(theObject):
                    xyCandidates[name] = theObject[:, 0]

        # based on the shape, find the compatible x and y axis candidates
        self.xCandidates = OrderedDictMod()
        self.yCandidates = OrderedDictMod()
        ydim, xdim = self._principalZ.data.shape

        # Case 1: length of x and y axis are equal, x and y share the same
        # compatible candidates
        if ydim == xdim:
            compatibleCandidates = OrderedDictMod({
                key: value for key, value in xyCandidates.items()
                if len(value) == xdim
            })
            self.xCandidates = self.yCandidates = compatibleCandidates
        
        # Case 2: length of x and y axis are not equal, the x and y axis can 
        # be distinguished by the length of the data
        else:
            for name, data in xyCandidates.items():
                if len(data) == xdim:
                    self.xCandidates[name] = data
                if len(data) == ydim:
                    self.yCandidates[name] = data

        # finally, insert pixel coordinates as the last resort
        self._addPixelCoord()

    def _initXYZ(self):
        """
        From the raw data, find the zData, xData, and yData candidates and their compatibles.
        """
        self.zCandidates = self._findZCandidates(self.rawData)
        self._principalZ = self.zCandidates.itemByIndex(0)

        self._findXYCandidates()
        self._initRawXY()
        self._resetPrincipalXY()
    
    # plotting =========================================================
    def generatePlotElement(self) -> MeshgridElement:
        """
        Generate a plot element from the current data
        """
        zData = self.principalZ.data

        if self._logColoring:
            zMin, zMax, _, _ = self.currentMinMax(zData)
            linthresh = max(abs(zMin), abs(zMax)) / 20.0
            norm = colors.SymLogNorm(
                linthresh=linthresh,    # the range within which the plot is linear (i.e. color map is linear)
                vmin=zMin,
                vmax=zMax,  # **add_on_mpl_3_2_0
            )
        else:
            norm = None

        xData, yData = np.meshgrid(self.principalX.data, self.principalY.data)
        return MeshgridElement(
            "measurement",
            xData,
            yData,
            zData,
            norm = norm,
            rasterized = True,
            zorder = 0,
        )


class ImageMeasData(MeasurementData):
    """
    Class for storing and manipulating measurement data. The primary
    measurement data (zData) is expected to be a 3d float ndarray or a 2d
    float ndarray.

    Parameters
    ---------
    rawData: ndarray
        the raw data extracted from a data file, either a 2d or 3d array
    """
    rawData: np.ndarray

    def __init__(self, name: str, image: np.ndarray, file: str):
        super().__init__(name, image, file)
        self._initXYZ()

    def _initXYZ(self):
        """
        Cook up the x and y axis data from the raw data.
        """
        self.rawData = self._processRawZ(self.rawData)
        self.zCandidates = OrderedDictMod({self.name: self.rawData})
        self._principalZ = self.zCandidates.itemByIndex(0)

        # since there is no x and y axis data, we use pixel coordinates
        ydim, xdim = self._principalZ.data.shape[:2]
        self.xCandidates = OrderedDictMod(pixel_coord_1=np.arange(xdim))
        self.yCandidates = OrderedDictMod(pixel_coord_2=np.arange(ydim))
        self._addPixelCoord()
        self._initRawXY()
        self._resetPrincipalXY()

    def _processRawZ(self, zData: np.ndarray) -> np.ndarray:
        """
        Check the dimensions of the zData array and process it by
        - inversing the y axis
        """
        assert zData.ndim in [2, 3], "zData must be a 2d or 3d array"

        # inverse the y axis
        zData = np.flip(zData, axis=0)

        return zData

    def generatePlotElement(self, **kwargs) -> ImageElement:
        """
        Generate a plot element from the current data
        """
        return ImageElement(
            "measurement",
            self.principalZ.data,
            rasterized = True,
            zorder = 0,
        )


MeasDataType = Union[NumMeasData, ImageMeasData]
