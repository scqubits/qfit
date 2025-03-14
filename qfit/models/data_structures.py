from abc import ABC
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
from matplotlib import colors as colors

from qfit.utils.helpers import (
    OrderedDictMod,
)
from qfit.models.parameter_settings import ParameterType
from qfit.widgets.grouped_sliders import SLIDER_RANGE
from qfit.utils.helpers import OrderedDictMod, labelLinesWithNans
        

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
        The type of the status message, e.g. "ready", "error", "success",
        "warning", "computing", "initializing"
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
        initial: List[int | None],
        final: List[int | None],
        photons: Optional[int] = None,
    ): ...

    @overload
    def __init__(
        self,
        tagType: Literal["DISPERSIVE_BARE"],
        initial: List[Tuple[int, ...] | None],
        final: List[Tuple[int, ...] | None],
        photons: Optional[int] = None,
    ): ...

    def __init__(
        self,
        tagType: Literal["NO_TAG", "DISPERSIVE_DRESSED", "DISPERSIVE_BARE"] = "NO_TAG",
        initial: Optional[List[Tuple[int, ...] | None] | int] = None,
        final: Optional[List[Tuple[int, ...] | None] | int] = None,
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
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"ExtrTransition: {self.name}\n{self.data}"

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

    def __init__(
        self, 
        name: str, 
        z: np.ndarray, 
        fileName: str,
        **kwargs
    ):
        self.name = name
        self.z = z
        self.kwargs = kwargs
        self.fileName = fileName

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
        self, 
        name: str,
        x: np.ndarray, 
        y: np.ndarray, 
        z: np.ndarray, 
        fileName: str,
        **kwargs
    ):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.kwargs = kwargs
        self.fileName = fileName

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
        overall_specdata: List[SpectrumData],
        highlighted_specdata: List[SpectrumData],
    ):
        self.name = name
        self.overall_specdata = overall_specdata
        self.highlighted_specdata = highlighted_specdata
        
        assert len(self.overall_specdata) == len(self.highlighted_specdata)
        
    def __len__(self) -> int:
        return len(self.overall_specdata)
        
    def _plotOverallData(
        self, 
        axes: Axes,
        data: SpectrumData,
        alpha_factor: float = 1.0,
        zorder: float = -1,
        **kwargs
    ) -> None:
        fig = axes.get_figure()
        data.plot_evals_vs_paramvals(
            color="black",
            linewidth=2,
            linestyle="--",
            alpha=0.3 * alpha_factor,
            fig_ax=(fig, axes),
            zorder=zorder,
            **kwargs,
        )
        
    def _plotHighlightedData(
        self, 
        axes: Axes,
        data: SpectrumData,
        alpha_factor: float = 1.0,
        zorder: float = 1.0,
        xlim: Tuple[float, float] = None,
        ylim: Tuple[float, float] = None,
        **kwargs
    ) -> None:
        if len(data.param_vals) == 0: 
            return
        
        fig = axes.get_figure()
        
        artist_before = set(axes.get_children()) # help to get the Line2D artists
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            if data.energy_table.size > 0:

                # reset the cycler so that the colors are consistent
                axes.set_prop_cycle(cycler(color=[
                    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
                ]))

                data.plot_evals_vs_paramvals(
                    label_list=data.labels,
                    linewidth=2,
                    fig_ax=(fig, axes),
                    alpha=1.0 * alpha_factor,
                    zorder=zorder,
                    **kwargs,
                )
            else:
                # no highlighted data (usually when evalsCount too small)
                pass
         
        # get the line2D artists and label them 
        artist_after = set(axes.get_children())
        new_artists = list(artist_after - artist_before)
        line_artists = [artist for artist in new_artists if isinstance(artist, Line2D)]
        
        # select the lines that is within the xlim and ylim of the axis
        # and use some heuristics to find the positions of the labels
        # finally, label the lines
        labelLinesWithNans(axes, line_artists, xlim, ylim)

    def canvasPlot(
        self, 
        axes: Axes, 
        xlim: Tuple[float, float] = None,
        ylim: Tuple[float, float] = None,
        **kwargs
    ) -> None:
        """
        Plot the spectrum on the canvas
        """
        super().canvasPlot(axes, **kwargs)

        # since the scqubits backend do not return the artists, we need to
        # obtain the new artists by comparing the old and new artists
        artist_before = set(axes.get_children())
        
        alpha_factor_list = np.logspace(0, len(self)-1, len(self), base=0.5)
        zorder_list = np.linspace(3.0, len(self) * 3.0, len(self))    # spacing = 3 to fit in the labelLines
        for ov_data, hl_data, alpha_factor, zorder in zip(
            self.overall_specdata, 
            self.highlighted_specdata, 
            alpha_factor_list, 
            zorder_list
        ):
            self._plotOverallData(axes, ov_data, alpha_factor, zorder=-1, **kwargs)
            self._plotHighlightedData(axes, hl_data, alpha_factor, zorder=zorder, xlim=xlim, ylim=ylim, **kwargs)

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


emptyPlotElement = lambda name: PlotElement(name)


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
    
    def __repr__(self) -> str:
        data = ", ".join([f"{attr}: {getattr(self, attr)}" for attr in self.dataAttr])
        return f"{self.parent}.{self.name}: {data}"

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
        Store the value of the parameter from view. 
        If the source is a slider, the value should be denormalized before being stored.
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
        Store the value of the parameter from view.
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
        Store the value of the parameter from view.
        """
        if isinstance(value, str):
            convertedValue = self._toIntAsNeeded(float(value))
        elif isinstance(value, bool):
            convertedValue = value
        else:
            raise ValueError(f"Unknown type of value: {value}")

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
    

emptyMetaInfo = MeasMetaInfo("", "", (0, 0), [], [], [], [])

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
    
    
emptyConfig = MeasRawXYConfig()


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