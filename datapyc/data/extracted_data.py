# extracted_data.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from typing import Union

import numpy as np

from PySide2.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
)

import datapyc.io_utils.file_io_serializers as serializers

from datapyc.data.tagdata_view import Tag


class ActiveExtractedData(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas. In addition, it references calibration
    data to expose either the raw selected data, or their calibrated counterparts."""

    def __init__(self, data : np.ndarray = None):
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

    def data(self, index, role=Qt.DisplayRole):
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

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role=Qt.DisplayRole):
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
    QAbstractListModel, serializers.Serializable, metaclass=ListModelMeta
):
    def __init__(self):
        super().__init__()
        self.dataNames = ["dataset1"]
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList = [Tag()]
        self._calibrationFunc = None
        self._currentRow = 0

    def rowCount(self, *args) -> int:
        return len(self.dataNames)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            str_value = self.dataNames[index.row()]
            return str_value

    def setData(self, index, value, role=None):
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
        self.layoutChanged.emit()
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
        self.assocTagList[self.currentRow] = newTag

    def setCalibrationFunc(self, calibrationDataCallback):
        self._calibrationFunc = calibrationDataCallback

    def allDataSorted(self, applyCalibration):
        if applyCalibration:
            data = [self._calibrationFunc(dataSet) for dataSet in self.assocDataList]
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

    def serialize(self):
        """
        Convert the content of the current class instance into IOData format.

        Returns
        -------
        IOData
        """
        processedData = self.allDataSorted(applyCalibration=False)
        initdata = {
            "datanames": self.dataNames,
            "datalist": processedData,
            "taglist": self.assocTagList,
        }
        iodata = serializers.dict_serialize(initdata)
        iodata.typename = "DatapycData"
        return iodata
