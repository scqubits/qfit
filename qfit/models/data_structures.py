from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Dict, Any, Optional

import numpy as np
from scqubits.core.storage import SpectrumData
import warnings

from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
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
class PlotElement(ABC):
    artists: Union[Artist, List[Artist]]

    @abstractmethod
    def canvasPlot(self, **kwargs) -> None:
        pass

    def remove(self) -> None:
        """
        Remove the element from the canvas
        """
        if self.artists is None:
            return
        
        if isinstance(self.artists, list):
            for artist in self.artists:
                artist.remove()
        else:
            self.artists.remove()

class ImageElement(PlotElement):
    """
    Data structure for passing and plotting images
    """
    artists: AxesImage

    def __init__(
        self, 
        z: np.ndarray,
        **kwargs
    ):
        self.z = z
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes) -> None:
        """
        Plot the image on the canvas
        """
        self.artists = axes.imshow(self.z, **self.kwargs)

        axes.figure.canvas.draw()
    
class ScatterElement(PlotElement):
    """
    Data structure for passing and plotting lines
    """
    artists: PathCollection

    def __init__(
        self, 
        x: np.ndarray, 
        y: np.ndarray,
        **kwargs
    ):
        self.x = x
        self.y = y
        self.kwargs = kwargs

    def canvasPlot(self, axes: Axes) -> None:
        """
        Plot the scatter on the canvas
        """
        self.artists = axes.scatter(self.x, self.y, **self.kwargs)
        axes.figure.canvas.draw()
    
class SpectrumElement(PlotElement):
    """
    Data structure for passing and plotting spectra from scqubits
    """
    artists: List[Line2D]

    def __init__(
        self,
        overall_specdata: SpectrumData,
        highlighted_specdata: SpectrumData,

    ):
        self.overall_specdata = overall_specdata
        self.highlighted_specdata = highlighted_specdata

    def canvasPlot(self, axes: Axes) -> None:
        """
        Plot the spectrum on the canvas
        """
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
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.highlighted_specdata.plot_evals_vs_paramvals(
                label_list=self.highlighted_specdata.labels,
                linewidth=2,
                fig_ax=(fig, axes),
            )

        artist_after = set(axes.get_children())
        self.artists = list(artist_after - artist_before)

        axes.figure.canvas.draw()
