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


import abc
import copy
import distutils.version as version

from typing import Dict, Tuple, Union

import numpy as np
import skimage.filters
import skimage.morphology
import skimage.restoration

from matplotlib import colors as colors
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_laplace

from PySide6.QtCore import (
    Signal,
    Slot,
    QObject,
    QAbstractListModel,
    Qt,
    QAbstractListModel,
    QModelIndex,
)
from PySide6 import QtGui

from qfit.models.data_structures import PlotElement, ImageElement, MeshgridElement
from qfit.models.registry import Registry, Registrable, RegistryEntry
from qfit.utils.helpers import (
    DictItem,
    OrderedDictMod,
    hasIdenticalCols,
    hasIdenticalRows,
    isValid1dArray,
    isValid2dArray,
)

from typing import List


class ListModelMeta(type(QAbstractListModel), type(Registrable)):
    pass


class MeasDataSet(QAbstractListModel, Registrable, metaclass=ListModelMeta):
    readyToPlot = Signal(PlotElement)
    relimCanvas = Signal(np.ndarray, np.ndarray)
    updateRawXMap = Signal(dict)

    def __init__(self, measDatas: List["MeasurementDataType"]):
        super().__init__()

        self._data = measDatas
        self._currentRow: int = 0

    # inits ============================================================
    def dynamicalInit(self, measDatas: List["MeasurementDataType"]):
        self._data = measDatas
        self.checkValidity()
        
    def checkValidity(self):
        # all of the data must have the same x and y axis names
        xNames = self._data[0].rawXNames
        yNames = self._data[0].rawYNames

        for data in self._data:
            if data.rawXNames != xNames or data.rawYNames != yNames:
                raise ValueError("All data must have the same x and y axis names")
            

    # Properties =======================================================
    @property
    def figNames(self) -> List[str]:
        return [data.name for data in self._data]

    @property
    def rawXNames(self) -> List[str]:
        return self._data[0].rawXNames

    @property
    def rawYNames(self) -> List[str]:
        return self._data[0].rawYNames

    @property
    def currentRow(self) -> int:
        return self._currentRow

    @property
    def currentMeasData(self) -> "MeasurementDataType":
        return self._data[self._currentRow]
    
    @property
    def currentFigName(self) -> str:
        return self.currentMeasData.name

    def data(self, index: QModelIndex, role):
        """
        The NAME & Icon of the transition!
        """
        if role == Qt.DisplayRole:
            str_value = self._data[index.row()].name
            return str_value

        # if role == Qt.DecorationRole:
        #     icon1 = QtGui.QIcon()
        # icon1.addPixmap(
        #     QtGui.QPixmap(":/icons/svg/cil-list.svg"),
        #     QtGui.QIcon.Normal,
        #     QtGui.QIcon.Off,
        # )
        #     return icon1

    def rowCount(self, *args) -> int:
        return len(self._data)

    def isEmpty(self) -> bool:
        return self._data == []

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    # Signal & Slots ===================================================
    def emitReadyToPlot(self):
        self.readyToPlot.emit(self.currentMeasData.generatePlotElement())
    
    def emitRelimCanvas(self):
        self.relimCanvas.emit(
            self.currentMeasData.currentX.data,
            self.currentMeasData.currentY.data,
        )

    def emitRawXMap(self):
        self.updateRawXMap.emit({
            data.name: data.rawXByCurrentX for data in self._data
        })

    @Slot(bool)
    def toggleBgndSubtractX(self, value: bool):
        self.currentMeasData._bgndSubtractX = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleBgndSubtractY(self, value: bool):
        self.currentMeasData._bgndSubtractY = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleTopHatFilter(self, value: bool):
        self.currentMeasData._topHatFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleWaveletFilter(self, value: bool):
        self.currentMeasData._waveletFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleEdgeFilter(self, value: bool):
        self.currentMeasData._edgeFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleLogColoring(self, value: bool):
        self.currentMeasData._logColoring = value
        self.emitReadyToPlot()

    @Slot(float)
    def setZMin(self, value: float):
        self.currentMeasData._zMin = value / 100
        self.emitReadyToPlot()

    @Slot(float)
    def setZMax(self, value: float):
        self.currentMeasData._zMax = value / 100
        self.emitReadyToPlot()

    @Slot(int)
    def setCurrentZ(self, itemIndex: int):
        self.currentMeasData.setCurrentZ(itemIndex)
        self.emitReadyToPlot()
        self.emitRelimCanvas()

    @Slot()
    def swapXY(self):
        self.currentMeasData.swapXY()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

    # registry =========================================================
    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the attributes of the parameter
        """

        def dataSetter(value):
            self._data = value
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()

        return {
            "measDataSet.currentRow": RegistryEntry(
                name="measDataSet.currentRow",
                quantity_type="r+",
                getter=lambda: self._currentRow,
                setter=lambda value: setattr(self, "_currentRow", value),
            ),
            "measDataSet.data": RegistryEntry(
                name="measDataSet.data",
                quantity_type="r+",
                getter=lambda: self._data,
                setter=dataSetter,
            ),
        }


class MeasurementData(Registrable):
    """Abstract basis class to enforce implementation of a data type specific plot method"""

    # even if the ImageMeasurementData class does not use these, they are still required
    # for setting up the UI
    _zCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 2d ndarrays
    rawX: OrderedDictMod[str, np.ndarray] = OrderedDictMod()
    rawY: OrderedDictMod[str, np.ndarray] = OrderedDictMod()

    _currentZ: DictItem
    _currentX: DictItem
    _currentY: DictItem

    # filters
    _bgndSubtractX = False
    _bgndSubtractY = False
    _topHatFilter = False
    _waveletFilter = False
    _edgeFilter = False

    _logColoring = False
    _zMin = 0.0
    _zMax = 1.0

    def __init__(self, name: str, rawData):
        super().__init__()

        self.name: str = name
        self.rawData = rawData

    # properties =======================================================
    @property
    def currentZ(self) -> DictItem:
        """
        Return current dataset describing the z values (measurement data) with all filters etc. applied.

        Returns
        -------
        DataItem
        """
        zData = copy.copy(self._currentZ)

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
    def currentX(self) -> DictItem:
        """
        Return current dataset describing the x-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._currentX

    @property
    def currentY(self) -> DictItem:
        """
        Return current dataset describing the y-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._currentY

    def setCurrentZ(self, itemIndex):
        self._currentZ = self._zCandidates.itemByIndex(itemIndex)

    @property
    def rawXNames(self) -> List[str]:
        return self.rawX.keyList

    @property
    def rawYNames(self) -> List[str]:
        return self.rawY.keyList
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MeasurementData):
            return False

        # # compare dictionaries of numpy arrays
        # dictAttrs = [
        # ]
        # for attr in dictAttrs:
        #     selfAttr = getattr(self, attr)
        #     valueAttr = getattr(__value, attr)
        #     if not selfAttr.keys() == valueAttr.keys():
        #         return False
        #     for key in selfAttr.keys():
        #         if not np.all(selfAttr[key] == valueAttr[key]):
        #             return False

        # compare the rest of the attributes
        dataAttrs = [
            "name",
            "rawData",
            "_zCandidates",
            "rawX",
            "rawY",
            "_currentZ",
            "_currentX",
            "_currentY",
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

    # manipulation =====================================================
    @abc.abstractmethod
    def generatePlotElement(self) -> Union[ImageElement, MeshgridElement]:
        """
        Generate a plot element from the current data

        Returns
        -------
        PlotElement
        """
        pass

    def _transposeZ(self, array: np.ndarray) -> np.ndarray:
        if array.ndim == 2:
            return array.transpose()
        if array.ndim == 3:
            return array.transpose(1, 0, 2)

    def swapXY(self):
        if len(self.rawX) > 1:
            raise ValueError(
                "Cannot swap x and y axes if there are multiple x-axis candidates"
            )

        swappedZCandidates = {
            key: self._transposeZ(array) for key, array in self._zCandidates.items()
        }
        self._zCandidates = OrderedDictMod(swappedZCandidates)
        self._currentZ.data = self._transposeZ(self._currentZ.data)

        self.rawX, self.rawY = self.rawY, self.rawX
        self._currentX, self._currentY = self._currentY, self._currentX

    def rawXByCurrentX(self, currentX: float) -> OrderedDictMod[str, float]:
        """
        Return the raw x values corresponding to the current x values.

        Parameters
        ----------
        currentX: float
            current x value

        Returns
        -------
        OrderedDictMod[str, float]
        """
        fraction = (currentX - self.currentX.data[0]) / (
            self.currentX.data[-1] - self.currentX.data[0]
        )
        rawX = OrderedDictMod()
        for name, data in self.rawX.items():
            rawX[name] = data[0] + fraction * (data[-1] - data[0])
        return rawX

    # filters =============================================================
    def currentMinMax(self, array2D: np.ndarray) -> Tuple[float, float, float, float]:
        if array2D.ndim != 2:
            raise ValueError("array must be 2D")
        
        normedMin = min(self._zMin, self._zMax)
        normedMax = max(self._zMin, self._zMax)

        rawZMin = array2D.min()
        rawZMax = array2D.max()
        # Choose Z value range according to the range slider values.
        zMin = rawZMin + normedMin * (rawZMax - rawZMin)
        zMax = rawZMin + normedMax * (rawZMax - rawZMin)

        return zMin, zMax, rawZMin, rawZMax

    def _doBgndSubtraction(self, array: np.ndarray, axis=0):
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
        return skimage.restoration.denoise_wavelet(array, rescale_sigma=True)
    
    def _applyEdgeFilter(self, array: np.ndarray):
        # Check if the data is a 3D array
        if len(array.shape) == 3:
            # Apply the filter to each color channel separately
            for i in range(array.shape[2]):
                array[:, :, i] = gaussian_laplace(array[:, :, i], 1.0)
        else:
            array = gaussian_laplace(array, 1.0)

        return array
    
    def _applyTopHatFilter(self, array: np.ndarray):
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
    Class for storing and manipulating measurement data. The primary measurement data (zData) is expected to be a
    2d float ndarray representing, for example, a two-tone spectroscopy amplitude as a function of probe frequency
    and an external field such as flux.

    Parameters
    ---------
    rawData: list of ndarray
        list containing all 1d and 2d arrays (floats) extracted from a data file
    zCandidates: OrderedDictMod [str, ndarray]
        each dict entry records the name associated with the dataset, and the dataset element, which is a 2d ndarray
        of floats representing a possible set of measurement data (zData)
    """

    def __init__(
        self,
        name: str,
        rawData: OrderedDictMod[str, np.ndarray],
    ):
        """

        Parameters
        ----------
        rawData
        zCandidates: dict or OrderedDictMod
        """
        super().__init__(name, rawData)
        self._initXYZ()

    # initialization ===================================================
    @staticmethod
    def _findZCandidates(rawData: Union[OrderedDictMod, Dict]):
        """
        Find all 2d ndarrays in the rawData dict that are suitable as zData candidates.
        """
        zCandidates = OrderedDictMod()
        for name, theObject in rawData.items():
            if isinstance(theObject, np.ndarray) and isValid2dArray(theObject):
                if not (hasIdenticalCols(theObject) or hasIdenticalRows(theObject)):
                    zCandidates[name] = theObject

        # all zCandidates must have the same shape
        if len(set([z.shape for z in zCandidates.values()])) > 1:
            raise ValueError("zCandidates must have the same shape")

        return zCandidates

    def _findRawXY(self):
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
        self.rawX = OrderedDictMod()
        self.rawY = OrderedDictMod()
        ydim, xdim = self._currentZ.data.shape
        if ydim == xdim:
            raise NotImplementedError(
                "x and y dimensions are equal and currently not supported"
            )

        # insert the compatible x and y axis candidates into the respective dicts
        for name, data in xyCandidates.items():
            if len(data) == xdim:
                self.rawX[name] = data
            if len(data) == ydim:
                self.rawY[name] = data
        if not self.rawX:
            self.rawX = OrderedDictMod(pixel_x=np.arange(xdim))
        if not self.rawY:
            self.rawY = OrderedDictMod(pixel_y=np.arange(ydim))

        # based on the number of the compatible x and y axis candidates
        # determine the tuning axis and freq axis. Freq axis is the one
        # with only one compatible candidate.
        if len(self.rawY) == 1 and len(self.rawX) >= 1:
            # do nothing
            pass
        elif len(self.rawX) == 1 and len(self.rawY) > 1:
            self.swapXY()
        elif len(self.rawX) > 1 or len(self.rawY) > 1:
            raise NotImplementedError(
                "Multiple compatible x or y-axis data found and currently "
                "not supported. Will be supported in the next version."
            )

        # finally, determine the principal x axis - largest change in the data
        if len(self.rawX) > 1:
            idx = np.argmax(
                [
                    np.abs(data[-1] - data[0])
                    for data in self.rawX.values()
                ]
            )
            self._currentX = self.rawX.itemByIndex(idx)

    def _initXYZ(self):
        """
        From the raw data, find the zData, xData, and yData candidates and their compatibles.
        """
        self._zCandidates = self._findZCandidates(self.rawData)
        self._currentZ = self._zCandidates.itemByIndex(0)

        self._findRawXY()
        self._currentX = self.rawX.itemByIndex(0)
        self._currentY = self.rawY.itemByIndex(0)

    def setCurrentZ(self, itemIndex):
        self._currentZ = self._zCandidates.itemByIndex(itemIndex)

    # def setCurrentX(self, itemIndex):
    #     self._currentX = self.currentXCompatibles.itemByIndex(itemIndex)
    #     self.emitReadyToPlot()
    #     self.emitRelimCanvas()
        # self.emitRawXMap()
    
    # def setCurrentY(self, itemIndex):
    #     self._currentY = self.currentYCompatibles.itemByIndex(itemIndex)
    #     self.emitReadyToPlot()
    #     self.emitRelimCanvas()
        # self.emitRawXMap()
        
    def generatePlotElement(self) -> MeshgridElement:
        zData = self.currentZ.data

        if self._logColoring:
            zMin, zMax = self.currentMinMax(zData)
            linthresh = max(abs(zMin), abs(zMax)) / 20.0
            norm = colors.SymLogNorm(
                linthresh=linthresh,
                vmin=zMin,
                vmax=zMax,  # **add_on_mpl_3_2_0
            )
        else:
            norm = None

        xData, yData = np.meshgrid(self.currentX.data, self.currentY.data)
        return MeshgridElement(
            "measurement",
            xData,
            yData,
            zData,
            norm=norm,
            rasterized=True,
        )


class ImageMeasurementData(MeasurementData):
    rawData: np.ndarray

    def __init__(self, name: str, image: np.ndarray):
        super().__init__(name, image)
        self._initXYZ()

    def _initXYZ(self):
        self.rawData = self._processRawZ(self.rawData)
        self._zCandidates = OrderedDictMod({self.name: self.rawData})
        self._currentZ = self._zCandidates.itemByIndex(0)

        print(self._currentZ.data.shape)

        # note that the x and y axis for images are swapped
        ydim, xdim, _ = self._currentZ.data.shape
        self.rawX = OrderedDictMod(pixel_x=np.arange(xdim))
        self.rawY = OrderedDictMod(pixel_y=np.arange(ydim))
        self._currentX = self.rawX.itemByIndex(0)
        self._currentY = self.rawY.itemByIndex(0)

    def _processRawZ(self, zData: np.ndarray) -> np.ndarray:
        """
        Convert a 3d array to a 2d array by averaging over the third dimension.
        """
        assert zData.ndim in [2, 3], "zData must be a 2d or 3d array"

        # inverse the y axis
        zData = np.flip(zData, axis=0)

        return zData

    def generatePlotElement(self, **kwargs) -> ImageElement:
        return ImageElement(
            "measurement",
            self.currentZ.data,
            rasterized=True,
        )


MeasurementDataType = Union[NumericalMeasurementData, ImageMeasurementData]
