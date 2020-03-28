# measureddata_models.py
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

import numpy as np
from matplotlib import colors as colors
from scipy.ndimage import gaussian_laplace
from scipy.signal import savgol_filter

from datapyc.core.misc import (DataItem,
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
        self.applyInterpolation = False
        self.success = False

    def setupUiCallbacks(self, checkBoxCallbacks, plotRangeCallbacks):
        self.checkBoxCallbacks = checkBoxCallbacks
        self.plotRangeCallbacks = plotRangeCallbacks

    @property
    def currentX(self):
        return self._currentX

    @property
    def currentY(self):
        return self._currentY

    @property
    def currentZ(self):
        return self._currentZ

    def canvasPlot(self, axes, **kwargs):
        pass


class NumericalMeasurementData(MeasurementData):
    def __init__(self, rawData):
        super().__init__(rawData)
        self.zCandidates = self.findZData()
        if self.zCandidates:
            self._currentZ = self.zCandidates.itemByIndex(0)
            self.success = True
        self.inferXYData()

    @property
    def currentZ(self):
        zData = copy.copy(self._currentZ)
        if self.checkBoxCallbacks['swapXY']():
            zData.data = np.transpose(zData.data)

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
        if self.checkBoxCallbacks['swapXY']():
            return self._currentY
        return self._currentX

    @property
    def currentY(self):
        if self.checkBoxCallbacks['swapXY']():
            return self._currentX
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

    def findZData(self):
        zCandidates = OrderedDictMod()
        for name, theObject in self.rawData.items():
            if isinstance(theObject, np.ndarray) and isValid2dArray(theObject):
                if not (hasIdenticalCols(theObject) or hasIdenticalRows(theObject)):
                    zCandidates[name] = theObject
        return zCandidates

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
            norm = colors.SymLogNorm(linthresh=0.2, vmin=self.currentZ.data.min(), vmax=self.currentZ.data.max())
        else:
            norm = None

        if (self.currentX.data is None) or (self.currentY.data is None):
            _ = axes.pcolormesh(zData, vmin=zMin, vmax=zMax, norm=norm, **kwargs)
        else:
            _ = axes.pcolormesh(self.currentX.data, self.currentY.data, zData, vmin=zMin, vmax=zMax, norm=norm, **kwargs)


class ImageMeasurementData(MeasurementData):
    def __init__(self, fileName, image):
        super().__init__(None)
        self._currentZ = DataItem(fileName, image)
        self.zCandidates = {fileName: image}
        self.success = (image is not None)

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
            norm = colors.SymLogNorm(linthresh=0.2, vmin=self.currentZ.data.min(), vmax=self.currentZ.data.max())
        else:
            norm = None

        _ = axes.imshow(zData, vmin=zMin, vmax=zMax, norm=norm, **kwargs)
