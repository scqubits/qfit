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

from typing import Dict, Tuple, Union

import numpy as np
import skimage.filters
import skimage.morphology
import skimage.restoration

from matplotlib import colors as colors

from scipy.ndimage import gaussian_laplace

from PySide6.QtCore import (
    Signal,
    Slot,
    QAbstractListModel,
    Qt,
    QAbstractListModel,
    QModelIndex,
)

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
    """
    Model for the list of measurement data sets. It manages the addition,
    removal, and selection of measurement data sets. It also provides
    methods for manipulating the data sets, such as swapping x and y axes,
    applying filters, and setting the z value range.

    Parameters
    ----------
    measDatas: List[MeasurementDataType]
        list of measurement data with type NumericalMeasurementData or 
        ImageMeasurementData
    """
    readyToPlot = Signal(PlotElement)
    relimCanvas = Signal(np.ndarray, np.ndarray)
    updateRawXMap = Signal(dict)

    def __init__(self, measDatas: List["MeasurementDataType"]):
        super().__init__()

        self._data = measDatas
        self._currentRow: int = 0

    # inits ============================================================
    def replaceMeasData(self, measData: List["MeasurementDataType"]):
        """
        Update the measurement data, and emit the readyToPlot, relimCanvas,
        and updateRawXMap signals.

        Note: For the moment, when the measurement data is updated, all of the 
        properties will be re-initialized.
        """
        self._data = measData
        self._currentRow = 0

        self.checkValidity()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitReadyToPlot()

    def checkValidity(self):
        """
        Check if the data is valid:
            - all of the data must have the same x and y axis names

        If the data is not valid, raise a ValueError.
        """
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
        The NAME & Icon of the measurement data set!
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
        """
        Emit the readyToPlot signal with the current plotting element.
        """
        self.readyToPlot.emit(self.currentMeasData.generatePlotElement())
    
    def emitRelimCanvas(self):
        """
        Emit the relimCanvas signal with the current x and y axis data,
        which will be used to relim the canvas, set x snap values.
        """
        self.relimCanvas.emit(
            self.currentMeasData.principalX.data,
            self.currentMeasData.principalY.data,
        )

    def emitRawXMap(self):
        """
        Emit the updateRawXMap signal with the raw x values corresponding
        to the current x values.
        """
        self.updateRawXMap.emit({
            data.name: data.rawXByPrincipalX for data in self._data
        })

    @Slot(bool)
    def toggleBgndSubtractX(self, value: bool):
        """
        Toggle the background subtraction for the x axis, and emit the
        readyToPlot signal.
        """
        self.currentMeasData._bgndSubtractX = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleBgndSubtractY(self, value: bool):
        """
        Toggle the background subtraction for the y axis, and emit the
        readyToPlot signal.
        """
        self.currentMeasData._bgndSubtractY = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleTopHatFilter(self, value: bool):
        """
        Toggle the top hat filter, and emit the readyToPlot signal.
        """
        self.currentMeasData._topHatFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleWaveletFilter(self, value: bool):
        """
        Toggle the wavelet filter, and emit the readyToPlot signal.
        """
        self.currentMeasData._waveletFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleEdgeFilter(self, value: bool):
        """
        Toggle the edge filter, and emit the readyToPlot signal.
        """
        self.currentMeasData._edgeFilter = value
        self.emitReadyToPlot()

    @Slot(bool)
    def toggleLogColoring(self, value: bool):
        """
        Toggle the log coloring, and emit the readyToPlot signal.
        """
        self.currentMeasData._logColoring = value
        self.emitReadyToPlot()

    @Slot(float)
    def setZMin(self, value: float):
        """
        Set the minimum z value, and emit the readyToPlot signal.
        """
        self.currentMeasData._zMin = value / 100
        self.emitReadyToPlot()

    @Slot(float)
    def setZMax(self, value: float):
        """
        Set the maximum z value, and emit the readyToPlot signal.
        """
        self.currentMeasData._zMax = value / 100
        self.emitReadyToPlot()

    @Slot(int)
    def setPrincipalZ(self, itemIndex: int):
        """
        Set the current measurement data, and emit the readyToPlot signal, 
        and relimCanvas signal.
        """
        self.currentMeasData.setPrincipalZ(itemIndex)
        self.emitReadyToPlot()
        self.emitRelimCanvas()

    @Slot(str)
    def switchMeasData(self, figName: str):
        """
        Switch the current measurement data by the name, and emit the
        readyToPlot, relimCanvas, and updateRawXMap signals.
        """
        for i, data in enumerate(self._data):
            if data.name == figName:
                self._currentRow = i
                break

        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

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

    # registry =========================================================
    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all of the measurement data.
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
    _zCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 2d ndarrays
    _xCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 1d ndarrays
    _yCandidates: OrderedDictMod[
        str, np.ndarray
    ] = OrderedDictMod()  # dict of 1d ndarrays

    # raw data: the selected x, y, and z data, indicating the actual tuning
    # parameters and the measurement data
    _rawXNames: List[str]
    _rawYName: List[str]
    rawX: OrderedDictMod[str, np.ndarray] = OrderedDictMod()
    rawY: OrderedDictMod[str, np.ndarray] = OrderedDictMod()

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
    _zMax = 1.0

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
        zData = copy.copy(self._principalZ)

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
        return self.rawX.keyList

    @property
    def rawYNames(self) -> List[str]:
        return self.rawY.keyList
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MeasurementData):
            return False

        dataAttrs = [
            "name",
            "rawData",
            "_zCandidates",
            "_xCandidates",
            "_yCandidates",
            "_rawXNames",
            "_rawYName",
            "rawX",
            "rawY",
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
        yName: str,
    ):
        """
        Given the names of the x axis candidates, set the raw x axis names and
        the principal x axis.
        """
        # check if the names are valid
        if not all([name in self._xCandidates.keyList for name in xNames]):
            raise ValueError("Invalid raw x axis names as not all are in "
                             "the x axis candidate list")
        if yName not in self._yCandidates.keyList:
            raise ValueError("Invalid raw y axis name as it is not in the y "
                             "axis candidate list")
        if yName in xNames:
            raise ValueError("The raw x and y axis names must be different")

        self._rawXNames = xNames
        self._rawYName = [yName]

        # reset the principal x axis
        self._resetPrincipalXY()

    def setPrincipalZ(self, item: int | str):
        """
        Set the principal z dataset by the index or the name of the data.
        """
        if isinstance(item, str):
            itemIndex = self._zCandidates.keyList.index(item)
        self._principalZ = self._zCandidates.itemByIndex(itemIndex)
        
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
        # if the user have already selected multiple x axes, we will only
        # keep the first one, as y axis is unique
        self._rawXNames = self._rawXNames[:1]

        swappedZCandidates = {
            key: self._transposeZ(array) for key, array in self._zCandidates.items()
        }
        self._zCandidates = OrderedDictMod(swappedZCandidates)
        self._principalZ.data = self._transposeZ(self._principalZ.data)

        self._xCandidates, self._yCandidates = self._yCandidates, self._xCandidates
        self._rawXNames, self._rawYName = self._rawYName, self._rawXNames
        self._resetPrincipalXY()

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
        
        normedMin = min(self._zMin, self._zMax)
        normedMax = max(self._zMin, self._zMax)

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
    def rawX(self):
        return OrderedDictMod({
            key: value for key, value in self._xCandidates.items() 
            if key in self._rawXNames
        })
    
    @property
    def rawY(self):
        return OrderedDictMod({
            key: value for key, value in self._yCandidates.items()
            if key in self._rawYName
        })

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
        self._xCandidates = OrderedDictMod()
        self._yCandidates = OrderedDictMod()
        ydim, xdim = self._principalZ.data.shape

        # Case 1: length of x and y axis are equal, x and y share the same
        # compatible candidates
        if ydim == xdim:
            compatibleCandidates = OrderedDictMod({
                key: value for key, value in xyCandidates.items()
                if len(value) == xdim
            })
            self._xCandidates = self._yCandidates = compatibleCandidates
        
        # Case 2: length of x and y axis are not equal, the x and y axis can 
        # be distinguished by the length of the data
        else:
            for name, data in xyCandidates.items():
                if len(data) == xdim:
                    self._xCandidates[name] = data
                if len(data) == ydim:
                    self._yCandidates[name] = data

        # finally, insert pixel coordinates as the last resort
        self._xCandidates.update({"pixel_coord_1": np.arange(xdim)})
        self._yCandidates.update({"pixel_coord_2": np.arange(ydim)})

    def _initRawXY(self):
        """
        Initialize the raw x and y axis by the first compatible x and y axis.
        """
        self._rawXNames = self._xCandidates.keyList[:1]
        self._rawYName = self._yCandidates.keyList[:1]

        # if rawX and rawY are the same, set rawY to the next compatible y axis.
        # It can always be done because there are pixel coordinates as the last 
        # resort
        if self._rawXNames == self._rawYName:
            self._rawYName = self._yCandidates.keyList[1:2]

    def _initXYZ(self):
        """
        From the raw data, find the zData, xData, and yData candidates and their compatibles.
        """
        self._zCandidates = self._findZCandidates(self.rawData)
        self._principalZ = self._zCandidates.itemByIndex(0)

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
            norm=norm,
            rasterized=True,
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
        self._zCandidates = OrderedDictMod({self.name: self.rawData})
        self._principalZ = self._zCandidates.itemByIndex(0)

        # since there is no x and y axis data, we use pixel coordinates
        ydim, xdim = self._principalZ.data.shape[:2]
        self._xCandidates = OrderedDictMod(pixel_coord_1=np.arange(xdim))
        self._yCandidates = OrderedDictMod(pixel_coord_2=np.arange(ydim))
        self._rawXNames = ["pixel_coord_1"]
        self._rawYName = ["pixel_coord_2"]
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
            rasterized=True,
        )


MeasurementDataType = Union[NumericalMeasurementData, ImageMeasurementData]
