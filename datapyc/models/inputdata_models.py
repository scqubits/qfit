# inputdata_models.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import abc
import copy
import distutils.version as version

import numpy as np
import matplotlib
from matplotlib import colors as colors
from scipy.ndimage import gaussian_laplace
from scipy.signal import savgol_filter

import datapyc.io.file_io_serializers as serializers

from datapyc.core.helpers import (DataItem,
                                  OrderedDictMod,
                                  isValid2dArray,
                                  hasIdenticalCols,
                                  hasIdenticalRows,
                                  isValid1dArray)


class MeasurementData(abc.ABC):
    """Abstract basis class to enforce implementation of a data type specific plot method"""
    def __init__(self, rawData):
        self.rawData = rawData
        self.checkBoxCallbacks = None
        self.plotRangeCallbacks = None
        self._currentX = DataItem('', None)
        self._currentY = DataItem('', None)
        self._currentZ = DataItem('', None)
        self.xyCandidates = OrderedDictMod()
        self.zCandidates = OrderedDictMod()
        self.currentXCompatibles = OrderedDictMod()
        self.currentYCompatibles = OrderedDictMod()

    def setupUiCallbacks(self, checkBoxCallbacks, plotRangeCallbacks):
        self.checkBoxCallbacks = checkBoxCallbacks
        self.plotRangeCallbacks = plotRangeCallbacks

    @property
    def currentX(self):
        """
        Return current dataset describing the x-axis values

        Returns
        -------
        DataItem
            where `<DataItem>.data` is a 1d ndarray of float
        """
        return self._currentX

    @property
    def currentY(self):
        """
        Return current dataset describing the y-axis values

        Returns
        -------
        DataItem
            where `<DataItem>.data` is a 1d ndarray of float
        """
        return self._currentY

    @property
    def currentZ(self):
        """
        Return current dataset describing the z values (measurement data)

        Returns
        -------
        DataItem
        """
        return self._currentZ

    def canvasPlot(self, axes, **kwargs):
        pass


class NumericalMeasurementData(MeasurementData, serializers.Serializable):
    """
    Class for storing and manipulating measurement data. The primary measurement data (zData) is expected to be a
    2d float ndarray representing, for example, a two-tone spectroscopy amplitude as a function of probe frequency
    and an external field such as flux.

    Parameters
    ---------
    rawData: list of ndarray
        list containing all 1d and 2d arrays (floats) extracted from a data file
    zCandidates: OrderedDictMod [str, ndarray]
        each dict entry records the name associated with the dataset, and the dataset element, which  is a 2d ndarray
        of floats representing a possible set of measurement data (zData)
    """
    def __init__(self, rawData, zCandidates):
        """

        Parameters
        ----------
        rawData
        zCandidates: dict or OrderedDictMod
        """
        super().__init__(rawData)
        self.zCandidates = OrderedDictMod(zCandidates)
        self._currentZ = self.zCandidates.itemByIndex(0)
        self.inferXYData()

    @property
    def currentZ(self):
        """
        Return current dataset describing the z values (measurement data) with all filters etc. applied.

        Returns
        -------
        DataItem
        """
        zData = copy.copy(self._currentZ)

        if self.checkBoxCallbacks['savgolFilterX']():
            zData.data = self.applySavitzkyGolayFilter(zData.data, axis=1)

        if self.checkBoxCallbacks['savgolFilterY']():
            zData.data = self.applySavitzkyGolayFilter(zData.data, axis=0)

        if self.checkBoxCallbacks['bgndSubtractX']():
            zData.data = self.doBgndSubtraction(zData.data, axis=1)

        if self.checkBoxCallbacks['bgndSubtractY']():
            zData.data = self.doBgndSubtraction(zData.data, axis=0)

        if self.checkBoxCallbacks['gaussLaplaceFilter']():
            zData.data = gaussian_laplace(zData.data, 1.0)
        return zData

    @property
    def currentX(self):
        """
        Return current dataset describing the x-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._currentX

    @property
    def currentY(self):
        """
        Return current dataset describing the y-axis values, taking into account the possibility of an x-y swap.

        Returns
        -------
        ndarray, ndim=1
        """
        return self._currentY

    def setCurrentZ(self, itemIndex):
        self._currentZ = self.zCandidates.itemByIndex(itemIndex)
        self.inferXYData()

    def setCurrentX(self, itemIndex):
        self._currentX = self.currentXCompatibles.itemByIndex(itemIndex)

    def setCurrentY(self, itemIndex):
        self._currentY = self.currentYCompatibles.itemByIndex(itemIndex)

    def inferXYData(self):
        self.xyCandidates = self.findXYData()
        self.setXYCompatibles()
        if self.currentXCompatibles:
            self._currentX = self.currentXCompatibles.itemByIndex(0)
        if self.currentYCompatibles:
            self._currentY = self.currentYCompatibles.itemByIndex(0)

    def setXYCompatibles(self):
        self.currentXCompatibles = OrderedDictMod()
        self.currentYCompatibles = OrderedDictMod()
        ydim, xdim = self._currentZ.data.shape
        for name, data in self.xyCandidates.items():
            if len(data) == xdim:
                self.currentXCompatibles[name] = data
            if len(data) == ydim:
                self.currentYCompatibles[name] = data

    def findXYData(self):
        xyCandidates = OrderedDictMod()
        for name, theObject in self.rawData.items():
            if isinstance(theObject, np.ndarray):
                if isValid1dArray(theObject):
                    xyCandidates[name] = theObject.flatten()
                if isValid2dArray(theObject) and hasIdenticalRows(theObject):
                    xyCandidates[name] = theObject[0]
                if isValid2dArray(theObject) and hasIdenticalCols(theObject):
                    xyCandidates[name] = theObject[:, 0]
        return xyCandidates

    def swapXY(self):
        swappedZCandidates = {key: array.transpose() for key, array in self.zCandidates.items()}
        self.zCandidates = OrderedDictMod(swappedZCandidates)
        self._currentZ.data = self._currentZ.data.transpose()

        self.currentXCompatibles, self.currentYCompatibles = self.currentYCompatibles, self.currentXCompatibles
        self._currentX, self._currentY = self._currentY, self._currentX

    def doBgndSubtraction(self, array, axis=0):
        avgArray = array - np.nanmean(array, axis=axis, keepdims=True)
        return avgArray

    def applySavitzkyGolayFilter(self, array, axis=0):
        newArray = savgol_filter(array, window_length=3, polyorder=1, axis=axis)
        return newArray

    def canvasPlot(self, axes, **kwargs):
        zData = self.currentZ.data
        rawZMin = zData.min()
        rawZMax = zData.max()

        # Extract zRange from range slider values
        zRange = (self.plotRangeCallbacks['left'](), self.plotRangeCallbacks['right']())
        # Choose Z value range according to the range slider values.
        zMin = rawZMin + zRange[0] * (rawZMax - rawZMin)
        zMax = rawZMin + zRange[1] * (rawZMax - rawZMin)

        if self.checkBoxCallbacks['logColoring']():
            linthresh = max(abs(zMin), abs(zMax)) / 20.0
            if version.LooseVersion(matplotlib.__version__) >= version.LooseVersion("3.2.0"):
                add_on_mpl_3_2_0 = {'base': 10}
            else:
                add_on_mpl_3_2_0 = {}
            norm = colors.SymLogNorm(linthresh=linthresh, vmin=zMin, vmax=zMax, **add_on_mpl_3_2_0)
        else:
            norm = None

        if (self.currentX.data is None) or (self.currentY.data is None):
            _ = axes.pcolormesh(zData, vmin=zMin, vmax=zMax, norm=norm, **kwargs)
        else:
            _ = axes.pcolormesh(self.currentX.data, self.currentY.data, zData, vmin=zMin, vmax=zMax,
                                norm=norm, **kwargs)


class ImageMeasurementData(MeasurementData, serializers.Serializable):
    def __init__(self, fileName, image):
        super().__init__(None)
        self._currentZ = DataItem(fileName, image)
        self.zCandidates = {fileName: image}

    def canvasPlot(self, axes, **kwargs):
        zData = np.sum(self.currentZ.data, axis=2) if (self.currentZ.data.ndim == 3) else self.currentZ.data
        rawZMin = zData.min()
        rawZMax = zData.max()

        # Extract zRange from range slider values
        zRange = (self.plotRangeCallbacks['left'](), self.plotRangeCallbacks['right']())
        # Choose Z value range according to the range slider values.
        zMin = rawZMin + zRange[0] * (rawZMax - rawZMin)
        zMax = rawZMin + zRange[1] * (rawZMax - rawZMin)

        if self.checkBoxCallbacks['logColoring']():
            if version.LooseVersion(matplotlib.__version__) >= version.LooseVersion("3.2.0"):
                add_on_mpl_3_2_0 = {'base': 10}
            else:
                add_on_mpl_3_2_0 = {}
            norm = colors.SymLogNorm(linthresh=0.2, vmin=self.currentZ.data.min(), vmax=self.currentZ.data.max(),
                                     **add_on_mpl_3_2_0)
        else:
            norm = None

        _ = axes.imshow(zData, vmin=zMin, vmax=zMax, norm=norm, **kwargs)

    def swapXY(self):
        pass
