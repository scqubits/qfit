# data_structures.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from typing import Callable, List, Optional, Tuple, Union

import numpy as np
from PySide6.QtCore import QAbstractListModel

from qfit.widgets.data_tagging import NO_TAG


class ListLike:
    _datastore: list

    def __getitem__(self, item):
        return self._datastore[item]

    def __contains__(self, item):
        return item in self._datastore

    def __len__(self):
        if self._datastore:
            return len(self._datastore)
        return 0

    def append(self, item: list):
        self._datastore = np.append(self._datastore, item)

    def insert(self, index: int, item: list):
        if len(self._datastore) < index:
            raise IndexError(
                "Invalid index for insertion (index exceeds length of " "array."
            )
        self._datastore.insert(index, item)


class Datapoint:
    def __init__(self, x, y, tag=NO_TAG):
        self.x = x
        self.y = y
        self.tag = tag

    def swapXY(self):
        return Datapoint(self.y, self.x, tag=self.tag)

    def xy(self):
        return self.x, self.y


class Calibration:
    def __init__(
        self,
        rawVec1: Optional[np.ndarray] = None,
        rawVec2: Optional[np.ndarray] = None,
        mapVec1: Optional[np.ndarray] = None,
        mapVec2: Optional[np.ndarray] = None,
    ):
        """
        Store calibration data for x and y axes, and provide methods to transform
        between uncalibrated and calibrated data.

        Parameters
        ----------
        rawVec1, rawVec2, mapVec1, mapVec2: ndarray
            Each of these is a two component vector (x,y) marking a point. The
            calibration maps rawVec1 -> mapVec1, rawVec2 -> mapVec2 with an
            affine-linear transformation:   mapVecN = alphaMat . rawVecN + bVec.
        """
        self.rawVec1 = rawVec1
        self.rawVec2 = rawVec2
        self.mapVec1 = mapVec1
        self.mapVec2 = mapVec2
        self.bVec = None
        self.alphaMat = None

        if all([rawVec1, rawVec2, mapVec1, mapVec2]):
            self.setCalibration(rawVec1, rawVec2, mapVec1, mapVec2)
        else:
            self.resetCalibration()

    def resetCalibration(self):
        self.setCalibration((1.0, 0.0), (0.0, 1.0), (1.0, 0.0), (0.0, 1.0))

    def setCalibration(
        self,
        rVec1: Tuple[float, float],
        rVec2: Tuple[float, float],
        mVec1: Tuple[float, float],
        mVec2: Tuple[float, float],
    ):
        x1, y1 = rVec1
        x2, y2 = rVec2
        x1p, y1p = mVec1
        x2p, y2p = mVec2

        alphaX = (x1p - x2p) / (x1 - x2)
        alphaY = (y1p - y2p) / (y1 - y2)

        self.bVec = np.asarray([x1p - alphaX * x1, y1p - alphaY * y1])
        self.alphaMat = np.asarray([[alphaX, 0.0], [0.0, alphaY]])
        self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2 = (
            rVec1,
            rVec2,
            mVec1,
            mVec2,
        )

    def allCalibrationVecs(
        self,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2

    def calibrate(self, datapoint: Datapoint) -> Datapoint:
        rawVec = np.asarray([datapoint.xy()])
        mVec = self.alphaMat @ rawVec + self.bVec
        return Datapoint(*mVec.tolist(), tag=datapoint.tag)

    def calibrationFunc(self, datapoint_list: List[Datapoint]) -> List[Datapoint]:
        return [self.calibrate(datapoint) for datapoint in datapoint_list]


class Database(ListLike, QAbstractListModel):
    def __init__(
        self,
        data: Optional[List[List[Datapoint]]] = None,
        calibrationFunc: Optional[Callable] = None,
        calibrationOn=False,
    ):
        super().__init__()
        self._datastore = data if data else [[]]
        self.calibrationFunc = calibrationFunc or (lambda x: x)
        self._calibrationOn = calibrationOn
        self._currentSetIndex = 0
        self.dataNames = [
            "dataset{}".format(str(index))
            for index, _ in enumerate(self._datastore)
        ]

    def __getitem__(self, index) -> List[Datapoint]:
        if self._calibrationOn:
            return self.calibrationFunc(self._datastore[index])
        return self._datastore[index]

    ####################################################################################
    # BEGIN: Methods required for pyside6 QAbstractTableModel
    def rowCount(self, *args) -> int:
        return len(self.dataNames)

    def data(self, index: QModelIndex, role: int, *args, **kwargs):
        idx = index.row()
        if role == Qt.DisplayRole:
            return self.dataNames[idx]

        if not self[idx]:
            return None

        if role == Qt.DecorationRole:
            icon1 = QtGui.QIcon()
            if self[idx][0].tag != NO_TAG:
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/24x24/cil-list.png"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            else:
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/24x24/cil-link-broken.png"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            return icon1

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    # END (methods required for QAbstractTableModel)
    ####################################################################################

    def isEmpty(self):
        if self._datastore == [[]]:
            return True
        return False

    @property
    def currentSetIndex(self):
        return self._currentSetIndex
    
    def currentSet(self) -> List[Datapoint]:
        return self[self.currentSetIndex]

    def setCurrentToFirst(self):
        if len(self) > 0:
            self._currentSetIndex = 0

    def setCurrentToLast(self):
        if len(self) > 0:
            self._currentSetIndex = len(self)

    def setCalibration(self, calibrationFunc: Callable):
        self.calibrationFunc = calibrationFunc

    def toggleCalibration(self):
        self._calibrationOn = not self._calibrationOn
        
    def swapXY(self, inplace=True):
        data = [[datapoint.swapXY() for datapoint in dataset] for dataset in self]
        if inplace:
            self._datastore = data
        else:
            return data
    
    def currentSetXY(self) -> np.ndarray:
        return np.array([datapoint.xy for datapoint in self[self.currentSetIndex]])

    def currentSetTags(self) -> np.ndarray:
        return np.array([datapoint.tag for datapoint in self[self.currentSetIndex]])

    def callback(self):
        return self
    