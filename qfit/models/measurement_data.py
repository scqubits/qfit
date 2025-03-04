# measurement_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory eof this source tree.
############################################################################

import os
from abc import abstractmethod
import numpy as np
from copy import copy, deepcopy

from typing import Dict, Tuple, Union, List, Any, Set

import skimage.morphology
import skimage.restoration
from matplotlib import colors as colors

from matplotlib.image import imread
from scipy.io import loadmat
from scipy.ndimage import gaussian_laplace
from skimage.filters import threshold_otsu
import h5py

from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
    QAbstractListModel,
    Qt,
    QModelIndex,
)
from PySide6.QtWidgets import QFileDialog, QMessageBox

from qfit.models.data_structures import (
    PlotElement,
    MeasMetaInfo,
    MeasRawXYConfig,
    ImageElement,
    MeshgridElement,
    FilterConfig,
    Status,
    emptyMetaInfo,
    emptyConfig,
    emptyPlotElement,
)
from qfit.models.registry import Registrable, RegistryEntry
from qfit.utils.helpers import (
    OrderedDictMod,
    DictItem,
    isValid1dArray,
    isValid2dArray,
    hasIdenticalCols,
    hasIdenticalRows,
    makeUnique,
)


class MeasFileReader:
    def fromFile(self, fileName):
        pass

    @staticmethod
    def isLikelyLabberFile(h5File):
        """
        Heuristic inspection to determine whether the h5 file might be from Labber.
        """
        if {"Data", "Instrument config", "Settings", "Step config"}.issubset(
            set(h5File)
        ):
            return True
        return False

    # @staticmethod
    # def isLikelyDatapycFile(h5File):
    #     # Heuristic inspection to determine whether the h5 file might be from qfit
    #     if "__type" in h5File.attrs.keys() and h5File.attrs["__type"] == "QfitData":
    #         return True
    #     return False


class ImageFileReader(MeasFileReader):
    def fromFile(self, fileName):
        """
        Use matplotlib to read image data from file.
        """
        _, fileStr = os.path.split(fileName)
        imageData = imread(fileName)

        return ImageMeasurementData(fileStr, imageData, fileName)


class GenericH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> "NumericalMeasurementData":
        """
        Read numerical data from h5 file. If the file is likely to be from Labber,
        use the LabberH5Reader. Otherwise, load all of the non-scalar datasets
        from the file.
        """
        with h5py.File(fileName, "r") as h5File:
            if self.isLikelyLabberFile(h5File):
                labberReader = LabberH5Reader()
                return labberReader.fromFile(fileName)

            # generic h5 file, attempt to read
            dataCollection = OrderedDictMod()

            def visitor_func(name, data):
                if isinstance(data, h5py.Dataset):
                    if data.shape != ():  # ignore scalar datasets
                        if data[:].dtype in [np.float32, np.float64]:
                            dataCollection[name] = data[:]

            h5File.visititems(visitor_func)

        _, fileStr = os.path.split(fileName)

        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class LabberH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> "NumericalMeasurementData":
        """
        Read numerical data from Labber h5 file. The file is assumed to have
        a specific structure, with the data stored in a dataset named "Data".
        The channel names are stored in a dataset named "Channel names".
        """
        with h5py.File(fileName, "r") as h5File:
            dataEntries = ["Data"]
            dataEntries += [name + "/Data" for name in h5File if name[0:4] == "Log_"]

            dataNames = []
            dataArrays = []
            dataCollection = OrderedDictMod()

            for entry in dataEntries:
                array = h5File[entry + "/Data"][:]
                if array.ndim != 3:
                    raise Exception(
                        "Error reading data file. Appears to be a Labber file, but its structure does not"
                        "match employed heuristics."
                    )
                dataArrays.append(array)

                names = h5File[entry + "/Channel names"][:]

                if isinstance(names[0], str):
                    dataNames.append(names)
                else:
                    newNames = []
                    for infoTuple in names:
                        newNames.append(
                            str(infoTuple[0], "utf-8")
                            + " "
                            + str(infoTuple[1], "utf-8")
                        )
                        names = newNames
                        dataNames.append(newNames)

                dataCollection[names[0] + " " + entry] = array[:, 0, 0]
                dataCollection[names[1] + " " + entry] = array[0, 1, :]
                dataCollection[names[2] + " " + entry] = array[:, 2, :]
                if len(names) == 4:
                    dataCollection[names[3] + " " + entry] = array[:, 3, :]

        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class MatlabReader(MeasFileReader):
    def fromFile(self, fileName) -> "NumericalMeasurementData":
        """
        Read numerical data from .mat file, using scipy.io.loadmat.
        """
        dataCollection = OrderedDictMod(loadmat(fileName))

        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class CSVReader(MeasFileReader):
    def fromFile(self, fileName):
        """
        Read numerical data from .csv file, using numpy.loadtxt.
        """
        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(
            fileStr,
            OrderedDictMod({fileName: np.loadtxt(fileName)}),
            fileName,
        )


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
    zCandidates: OrderedDictMod[str, ndarray]
        A dictionary of 2d ndarrays, which may be suitable as zData candidates
    rawX: OrderedDictMod[str, ndarray]
        A dictionary of 1d ndarrays, which has the same length. They are
        multiple tuning parameters.
    rawY: OrderedDictMod[str, ndarray]
        A dictionary of 1d ndarrays, which has the same length. We require
        that rawY has only one element, which is the frequency axis.
    """

    # candidates: all possible x, y, and z data that are compatible in shape
    zCandidates: OrderedDictMod[str, np.ndarray]  # dict of 2d ndarrays
    xCandidates: OrderedDictMod[str, np.ndarray]  # dict of 1d ndarrays
    yCandidates: OrderedDictMod[str, np.ndarray]  # dict of 1d ndarrays
    discardedKeys: List[str] = []

    # raw data: the selected x, y, and z data, indicating the actual tuning
    # parameters and the measurement data
    _rawXNames: List[str]
    _rawYNames: List[str]

    # principal data: the z data that are used to plot and the x, y data that
    # serves as coordinates in the plot
    _principalZ: DictItem
    _principalX: DictItem  # x axis that has the largest change
    _principalY: DictItem

    def __init__(self, figName: str, rawData, file: str):
        super().__init__()

        self.name: str = figName
        self.rawData = rawData
        self.file = file

        # candidates: all possible x, y, and z data that are compatible in shape
        self.zCandidates = OrderedDictMod()  # dict of 2d ndarrays
        self.xCandidates = OrderedDictMod()  # dict of 1d ndarrays
        self.yCandidates = OrderedDictMod()  # dict of 1d ndarrays

        # raw data: the selected x, y, and z data, indicating the actual tuning
        # parameters and the measurement data
        self._rawXNames = []
        self._rawYNames = []

        self._initFilters()

    def _initFilters(self):
        self._bgndSubtractX = False
        self._bgndSubtractY = False
        self._topHatFilter = False
        self._waveletFilter = False
        self._edgeFilter = False
        self._logColoring = False
        self._zMin = 0.0
        self._zMax = 100.0
        self._colorMapStr = "PuOr"  # it's a property stored in each data, but won't
        # be used in generatePlotElement. It's used in
        # the mpl canvas view to set the color map of the
        # entire canvas.

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
        return self._rawYNames

    @property
    def rawX(self):
        return OrderedDictMod(
            {
                key: value
                for key, value in self.xCandidates.items()
                if key in self._rawXNames
            }
        )

    @property
    def rawY(self):
        return OrderedDictMod(
            {
                key: value
                for key, value in self.yCandidates.items()
                if key in self._rawYNames
            }
        )

    @property
    def ambiguousZOrient(self) -> bool:
        """
        Return True if the zData is ambiguous in orientation, even if specifying
        the x and y axes. This can happen if the zData has the same number of
        rows and columns.
        """
        return self.principalZ.data.shape[0] == self.principalZ.data.shape[1]
    
    def isCollinearWith(self, other: "MeasurementData") -> bool:
        """
        Return True if the two measurement data are scanned through
        collinear axes on the rawX space.
        """
        assert self.rawX.keyList == other.rawX.keyList, "can't compare data with different rawX dimensions"
        
        if len(self.rawX) == 1:
            # 1D rawX space, always collinear
            return True
        
        if self.principalX.name != other.principalX.name:
            # as the principalX is the one with the largest change,
            # they must be the same if two axes are collinear
            return False
        
        # for the rest of the rawX, compute their linear function 
        # of the principalX, and check if they are the same
        for key in self.rawX.keyList:
            if key == self.principalX.name:
                continue
            slope = (self.rawX[key][-1] - self.rawX[key][0]) / (self.principalX.data[-1] - self.principalX.data[0])
            intercept = self.rawX[key][0] - slope * self.principalX.data[0]
            if not np.allclose(other.rawX[key], slope * other.principalX.data + intercept):
                return False
        return True
    
    # manipulation =====================================================
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MeasurementData):
            return False

        dataAttrs = [
            "name",
            "file",
            "zCandidates",
            "xCandidates",
            "yCandidates",
            "discardedKeys",
            "_rawXNames",
            "_rawYNames",
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
            "_colorMapStr",
        ]

        return all(
            [getattr(self, attr) == getattr(__value, attr) for attr in dataAttrs]
        )

    def generateMetaInfo(self) -> MeasMetaInfo:
        """
        Generate the meta information of the measurement data
        """
        return MeasMetaInfo(
            name=self.name,
            file=self.file,
            shape=self._principalZ.data.shape[:2],
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
        ...

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
            raise ValueError(
                "Invalid raw x axis names as not all are in "
                "the x axis candidate list"
            )
        if len(yNames) != 1:
            raise ValueError(
                "Invalid raw y axis names as there must be " "only one y axis"
            )
        if yNames[0] not in self.yCandidates.keyList:
            raise ValueError(
                "Invalid raw y axis name as it is not in the y " "axis candidate list"
            )
        if yNames[0] in xNames:
            raise ValueError("The raw x and y axis names must be different")

        self._rawXNames = xNames
        self._rawYNames = yNames

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
        self._rawYNames = self.yCandidates.keyList[:1]

        # if rawX and rawY are the same, set rawY to the next compatible y axis.
        # It can always be done because there are pixel coordinates as the last
        # resort
        if self._rawXNames == self._rawYNames:
            self._rawYNames = self.yCandidates.keyList[1:2]

    # def _removePixelCoord(self):
    #     """
    #     Remove pixel coordinates from the x and y axis candidates. That is
    #     needed when we need to swap XY and regenerate a new set of pixel
    #     coordinates.
    #     """
    #     self.xCandidates = OrderedDictMod(
    #         {
    #             key: value
    #             for key, value in self.xCandidates.items()
    #             if not key.startswith("pixel_coord")
    #         }
    #     )
    #     self.yCandidates = OrderedDictMod(
    #         {
    #             key: value
    #             for key, value in self.yCandidates.items()
    #             if not key.startswith("pixel_coord")
    #         }
    #     )

    #     # if the pixel coordinates are chosen to be the raw x and y axis,
    #     # reset the raw x and y axis
    #     reset = False
    #     for name in self._rawXNames:
    #         if name.startswith("pixel_coord"):
    #             reset = True
    #     for name in self._rawYNames:
    #         if name.startswith("pixel_coord"):
    #             reset = True
    #     if reset:
    #         self._initRawXY()
    #         self._resetPrincipalXY()

    def _addPixelCoord(self):
        """
        Add pixel coordinates as the last resort for x and y axis candidates.
        """
        ydim, xdim = self._principalZ.data.shape[:2]
        self.xCandidates.update({f"range({xdim})": np.arange(xdim)})
        self.yCandidates.update({f"range({ydim})": np.arange(ydim)})

    def _resetPrincipalXY(self):
        """
        The principal x axis corresponds to the x axis that has the
        largest change in the data.
        Since there should only be one y axis, the principal y axis is
        the first y axis.
        """
        if len(self.rawX) > 1:
            idx = np.argmax([data.max() - data.min() for data in self.rawX.values()])
            self._principalX = self.rawX.itemByIndex(int(idx))
        else:
            self._principalX = self.rawX.itemByIndex(0)

        self._principalY = self.rawY.itemByIndex(0)

    def swapXY(self):
        """
        Swap the x and y axes and transpose the zData array.
        """
        # self._removePixelCoord()

        # if the user have already selected multiple x axes, we will only
        # keep the first one, as y axis is unique
        self._rawXNames = self._rawXNames[:1]

        swappedZCandidates = {
            key: self._transposeZ(array) for key, array in self.zCandidates.items()
        }
        self.zCandidates = OrderedDictMod(swappedZCandidates)
        self._principalZ.data = self._transposeZ(self._principalZ.data)

        self.xCandidates, self.yCandidates = self.yCandidates, self.xCandidates
        self._rawXNames, self._rawYNames = self._rawYNames, self._rawXNames

        # self._addPixelCoord()
        self._resetPrincipalXY()

    def transposeZ(self):
        """
        Transpose the zData array without swapping the x and y axes. It should
        be used when the zData array is ambiguous in orientation - when the
        number of rows and columns are the same.
        """
        if not self.ambiguousZOrient:
            raise ValueError("The zData array is not ambiguous in orientation")

        self.zCandidates = OrderedDictMod(
            {key: self._transposeZ(array) for key, array in self.zCandidates.items()}
        )
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
            color=self._colorMapStr,
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


class NumericalMeasurementData(MeasurementData):
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
        acceptedKeys = (
            self.zCandidates.keyList
            + self.xCandidates.keyList
            + self.yCandidates.keyList
        )
        return [key for key in allKeys if key not in acceptedKeys]

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
            compatibleCandidates = OrderedDictMod(
                {
                    key: value
                    for key, value in xyCandidates.items()
                    if len(value) == xdim
                }
            )
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
                linthresh=linthresh,  # the range within which the plot is linear (i.e. color map is linear)
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
            self.file,
            norm=norm,
            rasterized=True,
            zorder=0,
        )


class ImageMeasurementData(MeasurementData):
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
        self.xCandidates = OrderedDictMod({
            f"range{xdim}": np.arange(xdim)})
        self.yCandidates = OrderedDictMod({
            f"range{ydim}": np.arange(ydim)})
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
            self.file,
            rasterized=True,
            zorder=0,
        )


MeasDataType = Union[NumericalMeasurementData, ImageMeasurementData]


class ListModelMeta(type(QAbstractListModel), type(Registrable)):
    pass


class MeasDataSet(QAbstractListModel, Registrable, metaclass=ListModelMeta):
    """
    Model for the list of measurement data sets. It manages the addition,
    removal, and selection of measurement data sets. It also provides
    methods for manipulating the data sets, such as
    - select Z data, a two dimension array
    - select X and Y axis, they are one-dimension-like arrays that has
        length compatible with Z data. Note that there may be multiple X axis
        while only one Y axis.
    - transpose Z. It's activated when only one X axis and one Y axis are
        selected.
    - apply filters and set the z value range.

    Parameters
    ----------
    measDatas: List[MeasurementDataType]
        list of measurement data with type NumericalMeasurementData or
        ImageMeasurementData
    """
    importFinished = False      # will be handled by MeasDataCtrl

    # data list management
    figSwitched = Signal(str)
    metaInfoChanged = Signal(MeasMetaInfo)
    rawXYConfigChanged = Signal(MeasRawXYConfig)
    updateStatus = Signal(Status)
    newFigAdded = Signal(list)
    dataLoaded = Signal(list)

    # single data processing
    readyToPlot = Signal(PlotElement)
    relimCanvas = Signal(np.ndarray, np.ndarray)
    updateRawXMap = Signal(dict)

    # register
    attrToRegister = [
        "_currentRow",
        "checkedRawX",
        "checkedRawY",
    ]

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self.fullData: List[MeasDataType] = []
        self._currentRow: int = 0

        self.checkedRawX: List[str] = []
        self.checkedRawY: List[str] = []

    # init & load data list ============================================
    def loadDataSet(self, measDataList: List[MeasDataType]):
        """
        Replace all the measurement data with the new data. It will emit the
        signals to update the view and proceed to the next stage.
        """
        self.fullData = measDataList

        # emit the signals to update the view
        self.emitMetaInfo()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitFigSwitched()

        # update the raw X and Y axis names
        self._clearRawXY()

        # gather the data names
        dataNames = [measData.name for measData in self.fullData]

        # emit to proceed to the next stage
        self.dataLoaded.emit(dataNames)

    @staticmethod
    def _rawDataFromFile(fileName) -> MeasDataType | None:
        """
        Read experimental data from file. It supports .h5, .mat, .csv, .jpg,
        .jpeg, .png files.

        Parameters
        ----------
        fileName: str
            Name of file to be read.

        Returns
        -------
        MeasurementDataType
            The data read from the file.
        """
        _, suffix = os.path.splitext(fileName)

        if suffix.lower() in (".h5", ".hdf5"):
            reader = GenericH5Reader()
        elif suffix.lower() in (".jpg", ".jpeg", ".png"):
            reader = ImageFileReader()
        elif suffix.lower() == ".mat":
            reader = MatlabReader()
        elif suffix.lower() == ".csv":
            reader = CSVReader()
        else:
            return None

        try:
            data = reader.fromFile(fileName)
        except ValueError:
            # can't identify the relavant measurement data
            return None

        return data

    def _measDataFromDialog(
        self,
        home: str | None = None,
        multiple: bool = True,
    ) -> List["MeasDataType"] | None:
        """
        Open a dialog to select a file, and then read the measurement data from
        the file. It will keep asking for files until a valid file is selected.
        Only break the loop when the user selects a valid file or cancels the
        dialog.

        Parameters
        ----------
        home : str
            the home directory to start the dialog
        multiple : bool
            whether to allow multiple files to be selected

        Returns
        -------
        List[MeasurementDataType] | None
            The data read from the file. If the user canceled the dialog,
            return None.
        """
        # configure the file dialog
        if home is None:
            home = os.path.expanduser("~")
        fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"

        while True:
            # start a loop of asking for files, only break the loop
            # when the user selects a valid file
            if multiple:
                fileNames, _ = QFileDialog.getOpenFileNames(
                    self.parent(), "Open", home, fileCategories
                )
            else:
                fileName, _ = QFileDialog.getOpenFileName(
                    self.parent(), "Open", home, fileCategories
                )
                fileNames = [fileName]

            if not fileNames:
                # user canceled the dialog
                return None

            measurementData = []
            for fileName in fileNames:
                measData = self._rawDataFromFile(fileName)

                if measData is None:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Error opening file.")
                    msg.setInformativeText(
                        "The heuristic inspection failed to identify suitable "
                        f"data inside the file {fileName}"
                    )
                    msg.setWindowTitle("Error")
                    _ = msg.exec_()
                    break  # break the loop and ask for files again
                else:
                    measurementData.append(measData)

            if len(measurementData) == len(fileNames):
                break  # break the loop if all files are successfully read

        return measurementData

    def _loadData(
        self,
        fileName: str | List[str] | None = None,
    ) -> Tuple[bool, List[str]]:
        """
        Load the data from the file using the file name. If the file name is
        not provided, open a dialog to select a file.

        Parameters
        ----------
        fileName: str | List[str] | None
            The name of the file to be loaded. If None, open a dialog to select
            a file. If a string or a list of strings, load the file with the
            file names. Inside the GUI, the user always uses a dialog.

        Returns
        -------
        bool
            False if user canceled the dialog, True otherwise.
        str | List[str] | None
            The file name or a list of file names to be loaded.

        """
        if fileName is not None:
            if isinstance(fileName, str):
                if not os.path.isfile(fileName):
                    self.updateStatus.emit(
                        Status(
                            statusSource="import",
                            statusType="error",
                            message=f"File '{fileName}' does not exist.",
                        )
                    )
                    return (
                        True,
                        [],
                    )  # continue opening the gui, while data is not loaded
            elif isinstance(fileName, list):
                for file in fileName:
                    if not os.path.isfile(file):
                        self.updateStatus.emit(
                            Status(
                                statusSource="import",
                                statusType="error",
                                message=f"File '{file}' does not exist.",
                            )
                        )
                        return True, []
            else:
                self.updateStatus.emit(
                    Status(
                        statusSource="import",
                        statusType="error",
                        message="measurementFileName must be a string or a list of strings.",
                    )
                )
                return True, []

        # read measurement files from dialog
        if fileName is None:
            measurementData = self._measDataFromDialog()
            if measurementData is None:
                # user canceled the dialog, return False to close the GUI
                return False, []

        # read measurement files from a single file name
        elif isinstance(fileName, str):
            data = self._rawDataFromFile(fileName)
            if data is None:
                self.updateStatus.emit(
                    Status(
                        statusSource="import",
                        statusType="error",
                        message=f"Can't load file '{fileName}'.",
                    )
                )
                return True, []
            measurementData = [data]

        # read measurement files from a list of file names
        else:
            measurementData = []
            for file in fileName:
                measData = self._rawDataFromFile(file)
                if measData is None:
                    self.updateStatus.emit(
                        Status(
                            statusSource="import",
                            statusType="error",
                            message=f"Can't load file '{file}'.",
                        )
                    )
                    return True, []
                measurementData.append(measData)

        oldDataNumber = len(self.fullData)
        # add the measurement data to the list
        self.fullData = self.fullData + measurementData

        # rename the measurement data with repeated names
        names = [measData.name for measData in self.fullData]
        uniqueNames = makeUnique(names)
        for measData, name in zip(self.fullData, uniqueNames):
            measData.name = name

        # get the new data names
        newDataNames = [measData.name for measData in self.fullData[oldDataNumber:]]

        if measurementData != []:
            # if there are new data loaded, emit the signals
            self.emitMetaInfo()
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()
            self.emitFigSwitched()

            # update the raw X and Y axis names
            self._clearRawXY()

        return True, newDataNames

    def removeDataFile(self, index: int) -> None:
        """
        Remove a data file from the list of files to be loaded.

        Parameters
        ----------
        index: int
            Index of the file to be removed.
        """
        self.fullData.pop(index)

        # if the current row is removed, set the current row to the first row
        if self._currentRow >= len(self.fullData):
            self._currentRow = 0

        self.emitMetaInfo()
        self.emitRawXYConfig()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitFigSwitched()

    # Qt view related ==================================================
    @property
    def figNames(self) -> List[str]:
        return [data.name for data in self.fullData]

    @property
    def currentRow(self) -> int:
        return self._currentRow

    @property
    def currentMeasData(self) -> "MeasDataType":
        return self.fullData[self._currentRow]

    @property
    def currentFigName(self) -> str:
        return self.currentMeasData.name

    def data(self, index: QModelIndex, role):
        """
        The NAME & Icon of the measurement data set!
        """
        if role == Qt.DisplayRole:
            str_value = self.fullData[index.row()].name
            return str_value

    def rowCount(self, *args) -> int:
        return len(self.fullData)

    def isEmpty(self) -> bool:
        return self.fullData == []

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    @Slot()
    def insertRow(self, filename: str | List[str] | None = None):
        """
        Insert a new row at the end of the table.
        """
        result, newDataNames = self._loadData(fileName=filename)
        if not result:
            return False

        self._currentRow = -1

        self.newFigAdded.emit(newDataNames)

        return True

    @Slot(int)
    def removeRow(self, row: int):
        """
        Remove a row from the table.
        """
        if self.rowCount() == 0:
            return False
        
        self.fullData.pop(row)

        if self.rowCount() == 0:
            pass
        elif row > self._currentRow:
            pass
        elif row == self._currentRow:
            self._currentRow = row
        else:
            self._currentRow -= 1

        self.emitRawXYConfig()
        self.emitMetaInfo()
        self.emitReadyToPlot()
        self.emitRelimCanvas()

        return True

    # Raw XY management ================================================
    @classmethod
    def isSubsetExclusively(
        cls,
        checkedAxes: List[str] | Set[str],
        candidates: List[str] | Set[str],
        otherCandidates: List[str] | Set[str],
    ) -> bool:
        """
        Return True if the currently checked raw axes are exclusively
        conpatible with the candidates (not compatible with the other axes).

        Parameters
        ----------
        checkedAxes: List[str]
            The names of the currently checked raw axes.
        candidates: List[str]
            The candidates for the corresponding axis.
        otherCandidates: List[str]
            The candidates for the other axis.

        Return
        ------
        bool
            True if the currently checked raw axes are exclusively
            conpatible with the candidates (not compatible with the other axes).
        """
        if len(checkedAxes) == 0:
            return False

        checkedSet = set(checkedAxes)
        return checkedSet.issubset(candidates) and not checkedSet.issubset(
            otherCandidates
        )

    @property
    def xCandidates(self) -> List[str]:
        """
        Get the raw X candidates from all data files. Currently, we show all
        of the X and Y axis candidates from all data files, and let the user
        select the X names.

        Returns
        -------
        List[str]
            The candidates for raw X axis names.
        """
        if not self.fullData:
            return []

        candidates = [
            set(data.xCandidates.keyList + data.yCandidates.keyList)
            for data in self.fullData
        ]
        candidates = set.intersection(*candidates)

        return list(candidates)

    @property
    def yCandidates(self) -> List[str]:
        """
        Get the raw Y candidates from all data files. Currently, we show all
        of the X and Y axis candidates from all data files, and let the user
        select the Y name -- the same as the X names.

        Returns
        -------
        List[str]
            The candidates for raw Y axis names -- the same as the X names.
        """
        return self.xCandidates

    @property
    def grayedRawX(self) -> List[str]:
        """
        Some of the raw X & raw Y configurations are not allowed, so we need to
        forbid the user to select invalid configurations by graying out some
        of the names.

        For X axes, we should gray out:
        - the names that are checked for Y axis
        - the names that are not compatible with the current selected X axis
            names.
        """
        checkedX = set(self.checkedRawX)
        checkedY = set(self.checkedRawY)

        # we will calculate a maximum set of grayed out X axis names, which
        # may contain the names that are not in X candidates:

        # the names that are checked for Y axis
        grayedX = set(self.checkedRawY)

        for data in self.fullData:
            xCompatible = set(data.xCandidates.keyList)
            yCompatible = set(data.yCandidates.keyList)

            # the names that are not compatible with the current selected X axis
            if self.isSubsetExclusively(checkedX, xCompatible, yCompatible):
                grayedX = grayedX.union(yCompatible)

            # the names that are only compatible with the current selected Y axis
            if self.isSubsetExclusively(checkedY, yCompatible, xCompatible):
                grayedX = grayedX.union(yCompatible)

        return list(grayedX)

    @property
    def grayedRawY(self) -> List[str]:
        """
        Some of the raw X & raw Y configurations are not allowed, so we need to
        forbid the user to select invalid configurations by graying out some
        of the names.

        For Y axes, we should gray out:
        - the names that are checked for X axis
        - the rest of the names, if the user has checked a name
        """
        checkedX = set(self.checkedRawX)

        # the names that are checked for X axis
        grayedY = set(self.checkedRawX)

        # the rest of names that are not checked for Y axis
        if len(self.checkedRawY) == 1:
            remainingCand = copy(self.yCandidates)
            remainingCand.remove(self.checkedRawY[0])
        else:
            remainingCand = []
        grayedY = grayedY.union(set(remainingCand))

        for data in self.fullData:
            xCompatible = set(data.xCandidates.keyList)
            yCompatible = set(data.yCandidates.keyList)

            # the names that are not compatible with the current selected X axis
            if self.isSubsetExclusively(checkedX, xCompatible, yCompatible):
                grayedY = grayedY.union(xCompatible)

        grayedY = grayedY.intersection(self.yCandidates)

        return list(grayedY)

    def _clearRawXY(self) -> None:
        """
        Initialize (clear) the raw X and Y axis names.
        """
        self.checkedRawX = []
        self.checkedRawY = []
        self.emitRawXYConfig()

    def _setRawXY(self, xNames: List[str], yNames: List[str]) -> None:
        """
        Set the raw X and Y axis names without sending any signals.

        Parameters
        ----------
        xNames: List[str]
            The raw X axis names.
        yNames: List[str]
            A one-element list of the raw Y axis name.
        """
        # the validity check should be done outside of this method
        self.checkedRawX = xNames
        self.checkedRawY = yNames

        if self._rawXYIsValid():
            for data in self.fullData:
                data.setRawXY(self.checkedRawX, self.checkedRawY)

    def _rawXYIsValid(self) -> bool:
        """
        Check if the selected raw X and Y axis names are valid. The raw X and
        Y axis names should be checked, and the user should select one X axis
        and one Y axis.

        Returns
        -------
        bool
            True if the raw X and Y axis names are valid, False otherwise.
        """
        xNames = set(self.checkedRawX)
        yNames = set(self.checkedRawY)

        # length
        if len(xNames) == 0 or len(yNames) != 1:
            return False

        # compatibility
        if not xNames.issubset(self.xCandidates):
            return False
        if not yNames.issubset(self.yCandidates):
            return False
        if len(xNames.intersection(self.grayedRawX)) > 0:
            return False
        if len(yNames.intersection(self.grayedRawY)) > 0:
            return False

        return True

    # Data list signals & slots ========================================
    @Slot(str)
    def switchFig(self, fig: str | int):
        """
        Switch the current measurement data by the name, and emit the
        readyToPlot, relimCanvas, and updateRawXMap signals.
        """
        if isinstance(fig, int):
            self._currentRow = fig
        else:
            for i, data in enumerate(self.fullData):
                if data.name == fig:
                    self._currentRow = i
                    break

        self.emitMetaInfo()
        self.emitRawXYConfig()  # update transpose button
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitFigSwitched()

    def emitMetaInfo(self):
        if self.rowCount() > 0:
            self.metaInfoChanged.emit(self.currentMeasData.generateMetaInfo())
        else:
            self.metaInfoChanged.emit(emptyMetaInfo)

    def emitFigSwitched(self):
        self.figSwitched.emit(self.currentFigName)

    def exportRawXYConfig(self) -> MeasRawXYConfig:
        """
        Export the raw X and Y axis names to view.

        Returns
        -------
        MeasRawXYConfig
            The configuration of raw X and Y axis names, including all of the
            candidates, selected X and Y axis names, and the names to be
            grayed out.
        """
        if self.rowCount() == 0:
            return emptyConfig
        
        return MeasRawXYConfig(
            checkedX=self.checkedRawX,
            checkedY=self.checkedRawY,
            xCandidates=self.xCandidates,
            yCandidates=self.yCandidates,
            grayedX=self.grayedRawX,
            grayedY=self.grayedRawY,
            allowTranspose=self.currentMeasData.ambiguousZOrient,
            allowContinue=self._rawXYIsValid() and len(self.fullData) > 0,
        )

    @Slot()
    def storeRawXYConfig(self, rawXYConfig: MeasRawXYConfig) -> None:
        """
        Store the raw X and Y axis names from view. There are a few cases
        to consider:
        - If the user has checked a name for X (Y), and this axis is actually
            corresponding Y axis in some data, swap the X and Y axis names for
            those data files and transpose Z.
        """
        # swap the X and Y axis names if necessary
        # note that it will re-init the stored raw XY info
        checkedX = rawXYConfig.checkedX
        checkedY = rawXYConfig.checkedY
        for data in self.fullData:
            swap = False
            if self.isSubsetExclusively(
                checkedX, data.yCandidates.keyList, data.xCandidates.keyList
            ):
                swap = True
            if self.isSubsetExclusively(
                checkedY, data.xCandidates.keyList, data.yCandidates.keyList
            ):
                swap = True

            if swap:
                data.swapXY()
                if data is self.currentMeasData:
                    self.emitMetaInfo()

        # store the raw X and Y axis names
        self._setRawXY(checkedX, checkedY)

        # gray out the X and Y axis names
        self.emitRawXYConfig()

        if self._rawXYIsValid():
            # update view
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()
        else:
            # some warning message?
            pass

    def emitRawXYConfig(self):
        self.rawXYConfigChanged.emit(self.exportRawXYConfig())

    # Single data signal & slots =======================================
    def emitReadyToPlot(self):
        """
        Emit the readyToPlot signal with the current plotting element.
        """
        if self.rowCount() > 0:
            self.readyToPlot.emit(self.currentMeasData.generatePlotElement())
        else:
            self.readyToPlot.emit(emptyPlotElement("measurement"))

    def emitRelimCanvas(self):
        """
        Emit the relimCanvas signal with the current x and y axis data,
        which will be used to relim the canvas, set x snap values.
        """
        if self.rowCount() == 0:
            self.relimCanvas.emit(np.array([0, 1]), np.array([0, 1]))
        else:
            self.relimCanvas.emit(
                self.currentMeasData.principalX.data,
                self.currentMeasData.principalY.data,
            )

    def emitRawXMap(self):
        """
        Emit the updateRawXMap signal with the raw x values corresponding
        to the current x values.
        """
        self.updateRawXMap.emit(
            {data.name: data.rawXByPrincipalX for data in self.fullData}
        )

    @Slot(FilterConfig)
    def storeFilter(self, filterConfig: FilterConfig):
        """
        Store the filter configuration, and emit the readyToPlot signal.
        """
        self.currentMeasData.setFilter(filterConfig)
        self.emitReadyToPlot()

    def exportFilter(self) -> FilterConfig:
        """
        Export the filter configuration to view.

        Returns
        -------
        FilterConfig
            The filter configuration.
        """
        return self.currentMeasData.getFilter()

    @Slot(int)
    def storePrincipalZ(self, itemIndex: int):
        """
        Set the current measurement data, and emit the readyToPlot signal,
        and relimCanvas signal.
        """
        self.currentMeasData.setPrincipalZ(itemIndex)
        self.emitReadyToPlot()
        self.emitRelimCanvas()

    @Slot()
    def swapXY(self):
        """
        Swap the x and y axes, and emit the readyToPlot, relimCanvas, and
        updateRawXMap signals.
        """
        self.currentMeasData.swapXY()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

    @Slot()
    def transposeZ(self):
        """
        Transpose the z axis, and emit the readyToPlot signal.
        """
        self.currentMeasData.transposeZ()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

    # registry =========================================================
    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all of the measurement data.
        """
        registryDict = {}
        for attr in self.attrToRegister:
            entry = self._toRegistryEntry(attr)
            registryDict[entry.name] = entry

        # full measurement data
        def dataSetter(value):
            self.fullData = value
            self.emitMetaInfo()
            self.emitRawXYConfig()
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()

        return registryDict | {
            "MeasDataSet.data": RegistryEntry(
                name="MeasDataSet.data",
                quantity_type="r+",
                getter=lambda: self.fullData,
                setter=dataSetter,
            ),
        }
