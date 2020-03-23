# datamodel.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import numpy as np
import scqubits.utils.file_io_serializers as serializers
from PySide2.QtCore import Slot, QAbstractTableModel, QAbstractListModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas. In addition, it references calibration
    data to expose either the raw selected data, or their calibrated counterparts."""
    def __init__(self, data=None):
        super().__init__()
        self._data = data or np.empty(shape=(2, 0), dtype=np.float_)
        self.calibrationModel = None

    @Slot()
    def all(self):
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
            conversionFunc = self.calibrationModel.conversionFunc()
            value = conversionFunc([self._data[0, index.column()], self._data[1, index.column()]])
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

    def headerData(self, section, orientation, role=Qt.DisplayRole):
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
                return str(['x', 'y'][section])
            elif orientation == Qt.Horizontal:
                return str(range(100)[section])

    def setData(self, index, value, role=Qt.EditRole):
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
    def setAllData(self, newData):
        """
        Replaces the current table of extracted data points with a new data set of points

        Parameters
        ----------
        newData: np.ndarray of float
            float array of data points to substitute the current data set
        """
        self._data = newData
        self.layoutChanged.emit()

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    def insertColumn(self, column, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertColumns(parent, column, column)
        self._data = np.insert(self._data, column, np.asarray([0., 0.]), axis=1)
        self.endInsertColumns()
        self.layoutChanged.emit()
        return True

    def removeColumn(self, column, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveColumns(parent, column, column)
        self._data = np.delete(self._data, column, axis=1)
        self.endRemoveColumns()
        self.layoutChanged.emit()
        return True

    def append(self, xval, yval):
        max_col = self.columnCount()
        self.insertColumn(max_col)
        self.setData(self.index(0, max_col), xval, role=Qt.EditRole)
        self.setData(self.index(1, max_col), yval, role=Qt.EditRole)
        self.layoutChanged.emit()

    def setCalibrationModel(self, calibrationModel):
        self.calibrationModel = calibrationModel


class ListModelMeta(type(QAbstractListModel), type(serializers.Serializable)):
    pass


class ListModel(QAbstractListModel, serializers.Serializable, metaclass=ListModelMeta):
    def __init__(self):
        super().__init__()
        self.dataList = ['dataset1']
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.calibrationModel = None
        self._currentRow = 0

    def rowCount(self, *args):
        return len(self.dataList)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            str_value = self.dataList[index.row()]
            return str_value

    def setData(self, index, value, role=None):
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self.dataList[index.row()] = value
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
        self.dataList.insert(row, '')
        self.assocDataList.insert(row, np.empty(shape=(2, 0), dtype=np.float_))
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        if self.rowCount() == 1:
            self.assocDataList[0] = np.empty(shape=(2, 0), dtype=np.float_)
            self.layoutChanged.emit()
            return True

        self.beginRemoveRows(parent, row, row)
        self.dataList.pop(row)
        self.assocDataList.pop(row)
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    @Slot()
    def newRow(self, str_value=None):
        rowCount = self.rowCount()
        str_value = str_value or 'dataset' + str(rowCount + 1)
        self.insertRow(rowCount)
        self.setData(self.index(rowCount, 0), str_value, role=Qt.EditRole)
        self.layoutChanged.emit()

    @Slot()
    def removeCurrentRow(self):
        self.removeRow(self.currentRow)

    @Slot()
    def removeAll(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.dataList = ['dataset1']
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
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

    @Slot()
    def updateAssocData(self, newData):
        self.assocDataList[self.currentRow] = newData

    def setCalibrationModel(self, calibrationModel):
        self.calibrationModel = calibrationModel

    def serialize(self):
        """
        Convert the content of the current class instance into IOData format.

        Returns
        -------
        IOData
        """
        initdata = {'datanames': self.dataList,
                    'datalist': self.assocDataList,
                    'calibration_data': self.calibrationModel}
        iodata = serializers.dict_serialize(initdata)
        iodata.typename = 'StoredFitData'
        return iodata
