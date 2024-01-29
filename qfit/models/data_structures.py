from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Dict, Any, Optional

import numpy as np
from scqubits.core.storage import SpectrumData
import warnings

from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.image import AxesImage
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

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

    def __init__(
        self, 
        name: str,
        z: np.ndarray,
        **kwargs
    ):
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
        self, 
        name: str,
        x: np.ndarray, 
        y: np.ndarray, 
        z: np.ndarray,
        **kwargs
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

    def __init__(
        self, 
        name: str,
        x: np.ndarray, 
        y: np.ndarray,
        **kwargs
    ):
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
            **kwargs
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.highlighted_specdata.plot_evals_vs_paramvals(
                label_list=self.highlighted_specdata.labels,
                linewidth=2,
                fig_ax=(fig, axes),
                **kwargs
            )

        artist_after = set(axes.get_children())
        self.artists = list(artist_after - artist_before)
        self.set_visible(self._visible)


class VLineElement(PlotElement):
    """
    Data structure for passing and plotting vertical lines
    """
    artists: List[Line2D]

    def __init__(
        self,
        name: str,
        x: Union[List[float], np.ndarray],
        **kwargs
    ):
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