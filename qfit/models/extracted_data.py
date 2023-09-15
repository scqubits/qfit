# extracted_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from typing import Union, Literal

import numpy as np
from PySide6 import QtGui

from PySide6.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
    Signal,
    QObject,
)

import qfit.io_utils.file_io_serializers as serializers

from qfit.widgets.data_tagging import NO_TAG, Tag

from qfit.models.registry import Registrable, RegistryEntry

from copy import deepcopy


class LoadFromRegistrySignal(QObject):
    signal = Signal(dict)


class ActiveExtractedData(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas. In
    addition, it references calibration data to expose either the raw selected data,
    or their calibrated counterparts."""

    def __init__(self, data: np.ndarray = None):
        """
        Parameters
        ----------
        data: np.ndarray
            numpy array of floats, shape=(2, N)
        """
        super().__init__()
        self._data = data or np.empty(shape=(2, 0), dtype=np.float_)
        self._adaptiveCalibrationFunc = None

    @Slot()
    def all(self) -> np.ndarray:
        """
        Return the raw data as a numpy array.

        Returns
        -------
        ndarray
        """
        return self._data

    @Slot()
    def toggleCalibratedView(self):
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        Return data at index `index` in string format, assuming that it is a float.

        Parameters
        ----------
        index: QModelIndex
            index of requested data
        role: int, default=QtCore.Qt.DisplayRole

        Returns
        -------
        str
        """
        if role == Qt.DisplayRole:
            conversionFunc = self._adaptiveCalibrationFunc()
            value = conversionFunc(
                [self._data[0, index.column()], self._data[1, index.column()]]
            )
            return "{:#.6g}".format(value[index.row()])

    def rowCount(self, *args):
        """
        Return number of rows.

        Returns
        -------
        int
        """
        return self._data.shape[0]

    def columnCount(self, *args):
        """
        Return number of columns.

        Returns
        -------
        int
        """
        return self._data.shape[1]

    def headerData(
        self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole
    ):
        """
        Obtain table header info in string format

        Parameters
        ----------
        section: int
        orientation: Qt.Orientation
        role: int

        Returns
        -------
        str
            String for the label of the horizontal or vertical header of the table.
        """
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return str(["x", "y"][section])
            elif orientation == Qt.Horizontal:
                return str(section)

    def setData(self, index: QModelIndex, value: float, role=Qt.EditRole) -> bool:
        """

        Parameters
        ----------
        index: QModelIndex
            index of element to be set to `value`
        value: float
        role: int

        Returns
        -------
        bool
            True if assignment successful
        """
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self._data[index.row(), index.column()] = value
        except (ValueError, IndexError):
            return False
        self.dataChanged.emit(index, index)
        return True

    @Slot()
    def setAllData(self, newData: Union[float, np.ndarray]):
        """
        Replaces the current table of extracted data points with a new dataset of points

        Parameters
        ----------
        newData: np.ndarray of float
            float array of data points to substitute the current data set
        """
        self._data = newData
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    def insertColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertColumns(parent, column, column)
        self._data = np.insert(self._data, column, np.asarray([0.0, 0.0]), axis=1)
        self.endInsertColumns()
        self.layoutChanged.emit()
        return True

    def removeColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveColumns(parent, column, column)
        self._data = np.delete(self._data, column, axis=1)
        self.endRemoveColumns()
        self.layoutChanged.emit()
        return True

    def append(self, xval: float, yval: float):
        max_col = self.columnCount()
        self.insertColumn(max_col)
        self.setData(self.index(0, max_col), xval, role=Qt.EditRole)
        self.setData(self.index(1, max_col), yval, role=Qt.EditRole)
        self.layoutChanged.emit()

    def setAdaptiveCalibrationFunc(self, adaptiveCalibrationCallback: callable):
        """
        Record the CalibrationData instance associated with the data.

        Parameters
        ----------
        adaptiveCalibrationCallback: function
        """
        self._adaptiveCalibrationFunc = adaptiveCalibrationCallback


class ListModelMeta(type(QAbstractListModel), type(serializers.Serializable)):
    pass


class AllExtractedData(
    QAbstractListModel, serializers.Serializable, Registrable, metaclass=ListModelMeta
):
    def __init__(self):
        super().__init__()
        self.dataNames = ["dataset1"]
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList = [Tag()]
        self._calibrationFunc = None
        self._currentRow = 0
        # this signal is used for updating the plot
        self.loadFromRegistrySignal = LoadFromRegistrySignal()

    def rowCount(self, *args) -> int:
        return len(self.dataNames)

    def data(self, index: QModelIndex, role):
        if role == Qt.DisplayRole:
            str_value = self.dataNames[index.row()]
            return str_value

        if role == Qt.DecorationRole:
            icon1 = QtGui.QIcon()
            if self.assocTagList[index.row()].tagType != NO_TAG:
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/svg/cil-list.svg"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            else:
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/svg/cil-link-broken.svg"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            return icon1

    def setData(self, index: QModelIndex, value, role=None):
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self.dataNames[index.row()] = value
        except (ValueError, IndexError):
            return False
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    def insertRow(self, row, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, row, row)
        self.dataNames.insert(row, "")
        self.assocDataList.insert(row, np.empty(shape=(2, 0), dtype=np.float_))
        self.assocTagList.insert(row, Tag())
        self.endInsertRows()
        return True

    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        if self.rowCount() == 1:
            self.assocDataList[0] = np.empty(shape=(2, 0), dtype=np.float_)
            self.assocTagList[0] = Tag()
            self.layoutChanged.emit()
            return True

        self.beginRemoveRows(parent, row, row)
        self.dataNames.pop(row)
        self.assocDataList.pop(row)
        self.assocTagList.pop(row)
        self.endRemoveRows()
        if self.currentRow == self.rowCount():
            self._currentRow -= 1
        self.layoutChanged.emit()
        return True

    def isEmpty(self):
        if len(self.assocDataList) == 1 and self.assocDataList[0].size == 0:
            return True
        return False

    def swapXY(self):
        swappedAssocDataList = [array[[1, 0]] for array in self.assocDataList]
        self.assocDataList = swappedAssocDataList

    @Slot()
    def newRow(self, str_value=None):
        rowCount = self.rowCount()
        str_value = str_value or "dataset" + str(rowCount + 1)
        counter = 1
        while str_value in self.dataNames:
            str_value = "dataset" + str(rowCount + 1 + counter)
        self.insertRow(rowCount)
        self.setData(self.index(rowCount, 0), str_value, role=Qt.EditRole)
        self.layoutChanged.emit()

    @Slot()
    def removeCurrentRow(self):
        self.removeRow(self.currentRow)

    @Slot()
    def removeAll(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.dataNames = ["dataset1"]
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList = [Tag()]
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    @property
    def currentRow(self):
        return self._currentRow

    @Slot()
    def setCurrentRow(self, index):
        self._currentRow = index.row()

    def currentItem(self):
        return self.data(self.index(self.currentRow, 0), role=Qt.EditRole)

    def currentAssocItem(self):
        return self.assocDataList[self.currentRow]

    def currentTagItem(self):
        return self.assocTagList[self.currentRow]

    @Slot()
    def updateAssocData(self, newData):
        self.assocDataList[self.currentRow] = newData

    @Slot()
    def updateCurrentTag(self, newTag):
        # print("updating: ", newTag)
        self.assocTagList[self.currentRow] = newTag

    def setCalibrationFunc(self, calibrationDataCallback):
        self._calibrationFunc = calibrationDataCallback

    def allDataSorted(
        self, applyCalibration, calibration_axis: Literal["xy", "x", "y"] = "xy"
    ):
        if applyCalibration:
            data = [
                self._calibrationFunc(dataSet, calibration_axis=calibration_axis)
                for dataSet in self.assocDataList
            ]
        else:
            data = self.assocDataList
        sortIndices = [np.argsort(xValues) for xValues, _ in data]
        xData = [dataSet[0] for dataSet in data]
        yData = [dataSet[1] for dataSet in data]
        sortedXData = [
            np.take(xValues, indices) for xValues, indices in zip(xData, sortIndices)
        ]
        sortedYData = [
            np.take(yValues, indices) for yValues, indices in zip(yData, sortIndices)
        ]
        allData = [
            np.asarray([xSet, ySet]).transpose()
            for xSet, ySet in zip(sortedXData, sortedYData)
        ]
        return allData

    def distinctSortedXValues(self):
        all_x_list = np.array([])
        for dataset in self.assocDataList:
            all_x_list = np.concatenate((all_x_list, dataset[0]))
        return np.sort(np.unique(all_x_list))

    def serialize(self):
        """
        Convert the content of the current class instance into IOData format.

        Returns
        -------
        IOData
        """
        processedData = self.allDataSorted(applyCalibration=False)
        initdata = {
            "dataNames": self.dataNames,
            "assocDataList": processedData,
            "assocTagList": self.assocTagList,
        }
        iodata = serializers.dict_serialize(initdata)
        iodata.typename = "QfitData"
        return iodata

    attrToRegister = [
        "dataNames",
        "assocDataList",
        "assocTagList",
    ]

    def registerAll(self):
        """
        Register necessary data for extracted data; these data are used to reconstruct the
        extracted data when loading a project file.
        """

        # info to be registered:
        # - dataNames
        # - assocDataList
        # - assocTagList
        def getter():
            # extracted_data = self.serialize()
            processedData = self.allDataSorted(applyCalibration=False)
            initdata = {
                "datanames": self.dataNames,
                "datalist": processedData,
                "taglist": self.assocTagList,
            }
            return deepcopy(initdata)

        def setter(initdata):
            # emit the signal to the controller to register the data through controller
            self.loadFromRegistrySignal.signal.emit(initdata)

        registry_entry = RegistryEntry(
            name="allExtractedData",
            quantity_type="r+",
            getter=getter,
            setter=setter,
        )
        registry = {"allExtractedData": registry_entry}
        return registry
