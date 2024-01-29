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


from typing import Union, Literal, List, Callable, Tuple

import numpy as np
from PySide6 import QtGui

from PySide6.QtCore import (
    QAbstractListModel,
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
    Signal,
)

from qfit.models.data_structures import Tag, ScatterElement, VLineElement

from qfit.models.registry import Registrable, RegistryEntry

from copy import deepcopy, copy

class ActiveExtractedData(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas. In
    addition, it references calibration data to expose either the raw selected data,
    or their calibrated counterparts."""

    dataUpdated = Signal(np.ndarray, Tag)
    dataSwitched = Signal(np.ndarray, Tag)
    readyToPlot = Signal(ScatterElement)

    def __init__(self, data: Union[np.ndarray, None] = None):
        """
        Parameters
        ----------
        data: np.ndarray
            numpy array of floats, shape=(2, N)
        """
        super().__init__()
        self._data: np.ndarray = data or np.empty(shape=(2, 0), dtype=np.float_)
        self._tag: Tag = Tag()
        self.connects()

    # Properties =======================================================
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

    @Slot()
    def allTransitions(self) -> np.ndarray:
        """
        Return the raw data as a numpy array.

        Returns
        -------
        ndarray
        """
        return self._data

    def isEmpty(self) -> bool:
        return self._data.size == 0
    
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
        
    # Internal data manipulation methods================================
    def insertColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
        # it will not emit custom signals 
        self.beginInsertColumns(parent, column, column)
        self._data = np.insert(self._data, column, np.asarray([0.0, 0.0]), axis=1)
        self.endInsertColumns()
        return True

    def removeColumn(self, column: QModelIndex, parent=QModelIndex(), *args, **kwargs):
        # it will not emit custom signals 
        self.beginRemoveColumns(parent, column, column)
        self._data = np.delete(self._data, column, axis=1)
        self.endRemoveColumns()
        return True

    def _updateData(self, index: QModelIndex, value: float, role=Qt.EditRole) -> bool:
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
        return True

    # Data manipulation ================================================
    def remove(self, index: int):
        """
        Public method to remove a point
        """
        self.removeColumn(index)
        self.emitDataUpdated()

    def append(self, xval: float, yval: float):
        """
        Public method to append a new point to the data set.
        """
        max_col = self.columnCount()
        self.insertColumn(max_col)
        self._updateData(self.index(0, max_col), xval, role=Qt.EditRole)
        self._updateData(self.index(1, max_col), yval, role=Qt.EditRole)
        self.emitDataUpdated()
    
    @Slot()
    def replaceAllData(self, newData: np.ndarray, newTag: Tag):
        """
        Replaces the current table of extracted data points with a new dataset of points

        Parameters
        ----------
        newData: np.ndarray of float
            float array of data points to substitute the current data set
        """
        self._data = newData
        self._tag = newTag
        self.emitDataSwitched()

    def updateTag(self, tag: Tag):
        """
        Set the tag of the data.

        Parameters
        ----------
        tag: Tag
        """
        self._tag = tag
        self.emitDataUpdated()

    def generatePlotElement(self) -> ScatterElement:
        # tag mode
        scat_active = ScatterElement(
            "active_extractions",
            self._data[0],
            self._data[1],
            marker=r"$\odot$",
            s=130,
            alpha=0.3,
        )
        return scat_active

    # Signal processing ================================================
    def emitDataUpdated(self):
        """
        view updated the model
        """
        self.dataUpdated.emit(self._data, self._tag)

    def emitDataSwitched(self):
        """
        model (allDatasets) switched it to a new data set
        """
        self.dataSwitched.emit(self._data, self._tag)

    def emitReadyToPlot(self):
        """
        Emit signal to update the plot
        """
        print("Active extracted data is ready to plot")
        self.readyToPlot.emit(self.generatePlotElement())

    def connects(self):
        self.dataUpdated.connect(self.emitReadyToPlot)
        self.dataSwitched.connect(self.emitReadyToPlot)


class ListModelMeta(type(QAbstractListModel), type(Registrable)):
    pass


class AllExtractedData(
    QAbstractListModel, Registrable, metaclass=ListModelMeta
):
    focusChanged = Signal(np.ndarray, Tag) # when user select and focus on a new row
    distinctXUpdated = Signal(np.ndarray) # when user extract (remove) data points
    readyToPlot = Signal(ScatterElement) # when user extract (remove) data points
    readyToPlotX = Signal(VLineElement) # when user extract (remove) data points
    loadedFromRegistry = Signal(dict) # when user load a project file

    def __init__(self):
        super().__init__()
        self.dataNames = ["Transition 1"]
        self.assocDataList: List[np.ndarray] = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList: List[Tag] = [Tag()]
        self._calibrationFunc = None
        self._currentRow = 0
        # this signal is used for updating the plot

    # Properties =======================================================
    def rowCount(self, *args) -> int:
        return len(self.dataNames)

    def currentItem(self):
        return self.data(self.index(self.currentRow, 0), role=Qt.EditRole)

    def currentAssocItem(self) -> np.ndarray:
        return self.assocDataList[self.currentRow]
    
    def allDataSorted(
        self, 
        removeCurrentRow: bool = False,
        applyCalibration: bool = True, 
        calibration_axis: Literal["xy", "x", "y"] = "xy",
        concat_data: bool = False,
    ) -> Union[List[np.ndarray], np.ndarray]:
        """
        Return all data points sorted by x value.

        Parameters
        ----------
        applyCalibration: bool, by default, True
            If True, apply the calibration function to the data points.
        calibration_axis: str, by default, "xy"
            If "xy", apply the calibration function to both x and y values.
            If "x", apply the calibration function to x values only.
            If "y", apply the calibration function to y values only.
        concat_data: bool, by default, False
            If True, concatenate all data points from different transitions 
            into a single array.

        Returns
        -------
        list of ndarray
            list of numpy arrays of length M, where M is the number
            of transitions. Each array may have shape (N, 2), where N is the 
            number of data points for each transition. If `concat_data` is True,
            then the output is a single numpy array of shape (~M*N, 2).
        """
        assocDataList = copy(self.assocDataList)
        if removeCurrentRow:
            assocDataList.pop(self.currentRow)

        if applyCalibration:
            data = [
                self._calibrationFunc(dataSet, calibration_axis=calibration_axis)
                for dataSet in assocDataList
            ]
        else:
            data = assocDataList

        allData = []
        for x, y in data:
            sorted_indices = np.argsort(x)
            allData.append(np.asarray([x[sorted_indices], y[sorted_indices]]).transpose())

        if allData == []:
            allData = [np.empty(shape=(0, 2), dtype=np.float_)]

        if concat_data:
            return np.concatenate(allData, axis=0)
        else:
            return allData

    def distinctSortedXValues(self):
        all_x_list = np.array([])
        for dataset in self.assocDataList:
            all_x_list = np.concatenate((all_x_list, dataset[0]))
        return np.sort(np.unique(all_x_list))

    def currentTagItem(self) -> Tag:
        return self.assocTagList[self.currentRow]
    
    def currentDataName(self) -> str:
        return self.dataNames[self.currentRow]
    
    def isEmpty(self) -> bool:
        for data in self.assocDataList:
            if data.size > 0:
                return False
        return True

    def data(self, index: QModelIndex, role):
        """
        The NAME & Icon of the transition!
        """
        if role == Qt.DisplayRole:
            str_value = self.dataNames[index.row()]
            return str_value

        if role == Qt.DecorationRole:
            icon1 = QtGui.QIcon()
            if self.assocTagList[index.row()].tagType != "NO_TAG":
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

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags
    
    # Signal processing ================================================
    def emitReadyToPlot(self, *args):
        print("All extracted data is ready to plot")
        self.readyToPlot.emit(self.generatePlotElement())

    def emitReadyToPlotX(self, *args):
        print("Xis ready to plot")
        self.readyToPlotX.emit(self.generatePlotElementX())

    def emitXUpdated(self, *args):
        """
        Update the distinct x values and send out plot data
        """
        self.distinctXUpdated.emit(self.distinctSortedXValues())
        self.emitReadyToPlotX()

    def connects(self):
        # focus changed --> update plot 
        self.focusChanged.connect(self.emitReadyToPlot)

    def setCalibrationFunc(self, calibrationDataCallback):
        self._calibrationFunc = calibrationDataCallback

    # Internal data manipulation methods ===============================
    def insertRow(self, row, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, row, row)
        self.dataNames.insert(row, "")
        self.assocDataList.insert(row, np.empty(shape=(2, 0), dtype=np.float_))
        self.assocTagList.insert(row, Tag())

        # update the current row before emitting the rowsRemoved signal 
        # (which will be emitted by endRemoveRows)
        self.setCurrentRow(row)

        self.endInsertRows()

        return True

    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        if self.rowCount() == 1:
            self.assocDataList[0] = np.empty(shape=(2, 0), dtype=np.float_)
            self.assocTagList[0] = Tag()
            self.setCurrentRow(0)
            return True

        self.beginRemoveRows(parent, row, row)
        self.dataNames.pop(row)
        self.assocDataList.pop(row)
        self.assocTagList.pop(row)

        # update the current row before emitting the rowsRemoved signal 
        # (which will be emitted by endRemoveRows)
        if row == self.rowCount():  # now row count is 1 less than before
            self.setCurrentRow(row - 1)
        else:
            self.setCurrentRow(row)

        self.endRemoveRows()

        return True

    # Data manipulation ================================================
    def updateName(self, index: QModelIndex, data, role=None):
        """
        Set the data at index `index` to `data`. Note that right now 
        data in the table is the name of the transition.
        """
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self.dataNames[index.row()] = data
        except (ValueError, IndexError):
            return False
        return True

    def swapXY(self):
        swappedAssocDataList = [array[[1, 0]] for array in self.assocDataList]
        self.assocDataList = swappedAssocDataList    
        self.emitXUpdated()
        self.emitReadyToPlot()

    @property
    def currentRow(self):
        return self._currentRow
    
    @Slot()
    def removeAll(self):
        """
        Remove all rows of dataset
        """
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.dataNames = ["Transition 1"]
        self.assocDataList = [np.empty(shape=(2, 0), dtype=np.float_)]
        self.assocTagList = [Tag()]

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        self.setCurrentRow(0)

        self.endRemoveRows()

        self.emitXUpdated()
        self.emitReadyToPlot()

        return True
    
    @Slot(str)
    def newRow(self, str_value=None):
        rowCount = self.rowCount()

        # find a unique name for the new row
        str_value = str_value or "Transition " + str(rowCount + 1)
        counter = 1
        while str_value in self.dataNames:
            str_value = "Transition " + str(rowCount + 1 + counter)
            counter += 1
        
        self.insertRow(rowCount)
        self.updateName(self.index(rowCount, 0), str_value, role=Qt.EditRole)
        self.emitReadyToPlot()

    @Slot()
    def removeCurrentRow(self):
        self.removeRow(self.currentRow)
        self.emitXUpdated()
        self.emitReadyToPlot()

    @Slot(np.ndarray, Tag)
    def updateAssocData(self, newData: np.ndarray, newTag: Tag):
        """
        Associted extracted data and tag updated from the active extracted data
        """
        self.assocDataList[self.currentRow] = newData
        self.assocTagList[self.currentRow] = newTag
        self.emitXUpdated()

    @Slot(int)
    def setCurrentRow(self, row: int):
        self._currentRow = row
        self.focusChanged.emit(
            self.currentAssocItem(), self.currentTagItem()
        )
    
    def generatePlotElement(self) -> ScatterElement:
        all_data = self.allDataSorted(
            applyCalibration=False,
            removeCurrentRow=True, 
            concat_data=True,
        )
        scat_all = ScatterElement(
            "all_extractions",
            all_data[:, 0],
            all_data[:, 1],
            marker=r"$\times$",
            s=70,
            alpha=0.23,
        )

        return scat_all
    
    def generatePlotElementX(self) -> VLineElement:

        vline_data = self.distinctSortedXValues()
        vline = VLineElement("extraction_vlines", vline_data, alpha=0.5)

        return vline

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
            # the reason for such special setter is that merely recovering the attributes
            # does not update the view correctly; additional steps are needed to update
            # the viewe accordingly through mainwindow
            self.loadedFromRegistry.emit(initdata)

        registry_entry = RegistryEntry(
            name="allExtractedData",
            quantity_type="r+",
            getter=getter,
            setter=setter,
        )
        registry = {"allExtractedData": registry_entry}
        return registry
