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


from typing import Callable, Optional, Union

import numpy as np
from PySide6 import QtGui

from PySide6.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
)

import qfit.io_utils.file_io_serializers as serializers
from qfit.core.data_structures import Database

from qfit.widgets.data_tagging import NO_TAG, Tag


class CurrentDatasetModel(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas. In
    addition, it references calibration data to expose either the raw selected data,
    or their calibrated counterparts."""

    def __init__(self, getCurrentSetFunc: Callable):
        """
        Parameters
        ----------
        data:
            Database of datasets of datapoints, including xy data and tagging
        """
        super(CurrentDatasetModel, self).__init__()
        self._getCurrentSetFunc = getCurrentSetFunc

    @property
    def dataset(self):
        return self._getCurrentSetFunc()
    
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
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            datapoint = self.dataset[col]
            value = datapoint.xy[row]
            return "{:#.6g}".format(value)

    def rowCount(self, *args):
        return 2

    def columnCount(self, *args):
        """
        Return number of columns.

        Returns
        -------
        int
        """
        return len(self.dataset)

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

    def flags(self, index: QModelIndex):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags


# class ActiveExtractedData2(QAbstractTableModel):
#     """This class holds one data set, as extracted by markers on the canvas. In
#     addition, it references calibration data to expose either the raw selected data,
#     or their calibrated counterparts."""
#
#     def __init__(self, data: Database):
#         """
#         Parameters
#         ----------
#         data:
#             Database of datasets of datapoints, including xy data and tagging
#         """
#         super().__init__()
#         self._datastore = data
#
#     @Slot()
#     def xy_data(self) -> np.ndarray:
#         """
#         Return the raw data as a numpy array.
#
#         Returns
#         -------
#         ndarray
#         """
#         if self._datastore and self._datastore.currentSetIndex():
#             return self._datastore.currentSetIndex().xy_data()
#         return None
#
#     @Slot()
#     def toggleCalibratedView(self):
#         self.layoutChanged.emit()
#
#     def data(self, index: QModelIndex, role=Qt.DisplayRole):
#         """
#         Return data at index `index` in string format, assuming that it is a float.
#
#         Parameters
#         ----------
#         index: QModelIndex
#             index of requested data
#         role: int, default=QtCore.Qt.DisplayRole
#
#         Returns
#         -------
#         str
#         """
#         if role == Qt.DisplayRole:
#             conversionFunc = self._adaptiveCalibrationFunc()
#             value = conversionFunc(
#                 [self._datastore[0, index.column()], self._datastore[1, index.column()]]
#             )
#             value = self._datastore.currentSetIndex()[index.column()].xy_data()
#             return "{:#.6g}".format(value[index.row()])
#
#     def rowCount(self, *args):
#         """
#         Return number of rows.
#
#         Returns
#         -------
#         int
#         """
#         return len(self._datastore.currentSetIndex())
#
#     def columnCount(self, *args):
#         """
#         Return number of columns.
#
#         Returns
#         -------
#         int
#         """
#         return 1
#         # return self._datastore.shape[1]
#
#     def headerData(
#         self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole
#     ):
#         """
#         Obtain table header info in string format
#
#         Parameters
#         ----------
#         section: int
#         orientation: Qt.Orientation
#         role: int
#
#         Returns
#         -------
#         str
#             String for the label of the horizontal or vertical header of the table.
#         """
#         # section is the index of the column/row.
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Vertical:
#                 return str(["x", "y"][section])
#             elif orientation == Qt.Horizontal:
#                 return str(section)
#
#     def setData(self, index: QModelIndex, value: float, role=Qt.EditRole) -> bool:
#         """
#
#         Parameters
#         ----------
#         index: QModelIndex
#             index of element to be set to `value`
#         value: float
#         role: int
#
#         Returns
#         -------
#         bool
#             True if assignment successful
#         """
#         if not (index.isValid() and role == Qt.EditRole):
#             return False
#         try:
#             self._datastore[index.row(), index.column()] = value
#         except (ValueError, IndexError):
#             return False
#         self.dataChanged.emit(index, index)
#         return True
#
#     @Slot()
#     def setAllData(self, newData: Union[float, np.ndarray]):
#         """
#         Replaces the current table of extracted data points with a new dataset of points
#
#         Parameters
#         ----------
#         newData: np.ndarray of float
#             float array of data points to substitute the current data set
#         """
#         self._datastore = newData
#         self.layoutChanged.emit()
#
#     def flags(self, index: QModelIndex):
#         flags = super(self.__class__, self).flags(index)
#         flags |= Qt.ItemIsEditable
#         flags |= Qt.ItemIsSelectable
#         flags |= Qt.ItemIsEnabled
#         return flags
#
#     def insertColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
#         self.beginInsertColumns(parent, column, column)
#         self._datastore = np.insert(self._datastore, column, np.asarray([0.0, 0.0]), axis=1)
#         self.endInsertColumns()
#         self.layoutChanged.emit()
#         return True
#
#     def removeColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
#         self.beginRemoveColumns(parent, column, column)
#         self._datastore = np.delete(self._datastore, column, axis=1)
#         self.endRemoveColumns()
#         self.layoutChanged.emit()
#         return True
#
#     def append(self, xval: float, yval: float):
#         max_col = self.columnCount()
#         self.insertColumn(max_col)
#         self.setData(self.index(0, max_col), xval, role=Qt.EditRole)
#         self.setData(self.index(1, max_col), yval, role=Qt.EditRole)
#         self.layoutChanged.emit()
#
#     def setAdaptiveCalibrationFunc(self, adaptiveCalibrationCallback: callable):
#         """
#         Record the CalibrationData instance associated with the data.
#
#         Parameters
#         ----------
#         adaptiveCalibrationCallback: function
#         """
#         self._adaptiveCalibrationFunc = adaptiveCalibrationCallback


class ListModelMeta(type(QAbstractListModel), type(serializers.Serializable)):
    pass


class AllDatasetsModel(QAbstractListModel):
    def __init__(self, getDatabaseFunc: Callable):
        super().__init__()
        self._getDatabaseFunc = getDatabaseFunc
        self.dataNames = [
            "dataset{}".format(str(index))
            for index, _ in enumerate(self.database)
        ]

    @property
    def database(self):
        return self._getDatabaseFunc()
    
    @property
    def currentSetIndex(self):
        return self.database.currentSetIndex

    def rowCount(self, *args) -> int:
        return len(self.dataNames)

    def data(self, index: QModelIndex, role: int, *args, **kwargs):
        if role == Qt.DisplayRole:
            str_value = self.dataNames[index.row()]
            return str_value

        dataset = self.database[index.row()]
        if not dataset:
            return None

        if role == Qt.DecorationRole:
            icon1 = QtGui.QIcon()
            if dataset[0].tag != NO_TAG:
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

    # def setData(self, index: QModelIndex, value, role=None):
    #     if not (index.isValid() and role == Qt.EditRole):
    #         return False
    #     try:
    #         self.dataNames[index.row()] = value
    #     except (ValueError, IndexError):
    #         return False
    #     self.dataChanged.emit(index, index)
    #     return True

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    # def insertRow(self, row, parent=QModelIndex(), *args, **kwargs):
    #     self.beginInsertRows(parent, row, row)
    #     self.dataNames.insert(row, "")
    #     self.assocDataList.insert(row, np.empty(shape=(2, 0), dtype=np.float_))
    #     self.assocTagList.insert(row, Tag())
    #     self.endInsertRows()
    #     return True
    #
    # def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
    #     if self.rowCount() == 1:
    #         self.assocDataList[0] = np.empty(shape=(2, 0), dtype=np.float_)
    #         self.assocTagList[0] = Tag()
    #         self.layoutChanged.emit()
    #         return True
    #
    #     self.beginRemoveRows(parent, row, row)
    #     self.dataNames.pop(row)
    #     self.assocDataList.pop(row)
    #     self.assocTagList.pop(row)
    #     self.endRemoveRows()
    #     if self.currentRow == self.rowCount():
    #         self.currentSet -= 1
    #     self.layoutChanged.emit()
    #     return True

    def isEmpty(self):
        if self.database[0]:
        # if len(self.assocDataList) == 1 and self.assocDataList[0].size == 0:
            return True
        return False

    def swapXY(self):
        pass
        # swappedAssocDataList = [array[[1, 0]] for array in self.assocDataList]
        # self.assocDataList = swappedAssocDataList

    @Slot()
    def newRow(self, str_value=None):
        pass
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
        pass
        self.removeRow(self.currentRow)

    @Slot()
    def removeAll(self):
        pass
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.dataNames = ["dataset1"]
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList = [Tag()]
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    @property
    def currentRow(self):
        return self.database.currentSet()

    @Slot()
    def setCurrentRow(self, index):
        pass
        self.currentSet = index.row()

    def currentItem(self):
        pass
        return self.data(self.index(self.currentRow, 0), role=Qt.EditRole)

    def currentAssocItem(self):
        pass
        return self.assocDataList[self.currentRow]

    def currentTagItem(self):
        pass
        return self.assocTagList[self.currentRow]

    @Slot()
    def updateAssocData(self, newData):
        pass
        self.assocDataList[self.currentRow] = newData

    @Slot()
    def updateCurrentTag(self, newTag):
        pass
        self.assocTagList[self.currentRow] = newTag

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
        iodata.typename = "QfitData"
        return iodata
