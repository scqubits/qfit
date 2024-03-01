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


from typing import Union, Literal, List, Callable, Tuple, overload, TYPE_CHECKING

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

from qfit.models.data_structures import (
    Tag,
    ExtrTransition,
    ExtrSpectra,
    FullExtr,
    ScatterElement,
    VLineElement,
)

from qfit.models.registry import Registrable, RegistryEntry

from copy import deepcopy, copy

if TYPE_CHECKING:
    from qfit.utils.helpers import OrderedDictMod


class ActiveExtractedData(QAbstractTableModel):
    """This class holds one data set, as extracted by markers on the canvas."""

    dataUpdated = Signal(ExtrTransition)
    dataSwitched = Signal(ExtrTransition)
    readyToPlot = Signal(
        ScatterElement
    )  # the above two signals are connected to this signal

    def __init__(self):
        """
        Parameters
        ----------
        data: np.ndarray
            numpy array of floats, shape=(2, N)
        """
        super().__init__()

        self._transition = ExtrTransition()

        self.connects()

    # Properties =======================================================
    def rowCount(self, *args):
        """
        Return number of rows.

        Returns
        -------
        int
        """
        return 2

    def columnCount(self, *args):
        """
        Return number of columns.

        Returns
        -------
        int
        """
        return self._transition.count()

    @Slot()
    def allPoints(self) -> np.ndarray:
        """
        Return the raw data as a numpy array.

        Returns
        -------
        ndarray
        """
        return self._transition.data

    def isEmpty(self) -> bool:
        return self._transition.count() == 0

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

    # Data manipulation ================================================
    def remove(self, index: int):
        """
        Public method to remove a point
        """
        self._transition.remove(index)
        self.emitDataUpdated()

    def append(
        self, xy: "OrderedDictMod[str, float]", rawX: "OrderedDictMod[str, float]"
    ):
        """
        Public method to append a new point to the data set.
        """
        self._transition.append(xy, rawX)
        self.emitDataUpdated()

    @Slot(ExtrTransition)
    def replaceAllData(self, newTransition: ExtrTransition):
        """
        Replaces the current table of extracted data points with a new dataset of points

        Parameters
        ----------
        newData: np.ndarray of float
            float array of data points to substitute the current data set
        """
        self._transition = newTransition
        self.emitDataSwitched()

    def updateTag(self, tag: Tag):
        """
        Set the tag of the data.

        Parameters
        ----------
        tag: Tag
        """
        self._transition.tag = tag
        self.emitDataUpdated()

    def generatePlotElement(self) -> ScatterElement:
        # tag mode
        scat_active = ScatterElement(
            "active_extractions",
            self._transition.data[0],
            self._transition.data[1],
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
        self.dataUpdated.emit(self._transition)

    def emitDataSwitched(self):
        """
        model (allDatasets) switched it to a new data set
        """
        self.dataSwitched.emit(self._transition)

    def emitReadyToPlot(self):
        """
        Emit signal to update the plot
        """
        self.readyToPlot.emit(self.generatePlotElement())

    def connects(self):
        self.dataUpdated.connect(self.emitReadyToPlot)
        self.dataSwitched.connect(self.emitReadyToPlot)


class ListModelMeta(type(QAbstractListModel), type(Registrable)):
    pass


class AllExtractedData(QAbstractListModel, Registrable, metaclass=ListModelMeta):
    dataUpdated = Signal(FullExtr)

    focusChanged = Signal(ExtrTransition)  # when user select and focus on a new row
    readyToPlot = Signal(ScatterElement)  # connected to the above signal

    distinctXUpdated = Signal(np.ndarray)  # when user extract (remove) data points
    readyToPlotX = Signal(VLineElement)  # connected to the above signal

    _figNames: List[str]
    _currentFigName: str
    _currentRow: int

    def __init__(self):
        super().__init__()

        self._fullSpectra = FullExtr()

        self.connects()

    def dynamicalInit(
        self,
        figNames: List[str],
    ):
        self._figNames = figNames
        self._initFullSpectra()

        self._currentFigName = self._figNames[0]
        self._currentRow = 0

    def _initSpectra(self, figName: str):
        transition = ExtrTransition()
        transition.name = "Transition 1"
        spectra = ExtrSpectra(
            transition,
        )
        self._fullSpectra[figName] = spectra

    def _initFullSpectra(self):
        for name in self._figNames:
            self._initSpectra(name)

    # Properties =======================================================
    @property
    def currentFigName(self):
        return self._currentFigName

    @property
    def currentRow(self):
        return self._currentRow

    @property
    def _currentSpectrum(self) -> ExtrSpectra:
        return self._fullSpectra[self.currentFigName]

    def data(self, index: QModelIndex, role):
        """
        The NAME & Icon of the transition!
        """
        if role == Qt.DisplayRole:
            str_value = self._currentSpectrum[index.row()].name
            return str_value

        if role == Qt.DecorationRole:
            icon1 = QtGui.QIcon()
            if self._currentSpectrum[index.row()].tag.tagType != "NO_TAG":
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/svg/tag.svg").scaled(40, 40),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            else:
                icon1.addPixmap(
                    QtGui.QPixmap(":/icons/svg/tag-question.svg").scaled(40, 40),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
            return icon1

    def rowCount(self, *args) -> int:
        return len(self._fullSpectra[self.currentFigName])

    def currentTransition(self) -> ExtrTransition:
        return self._currentSpectrum[self.currentRow]

    def isEmpty(self) -> bool:
        return self._currentSpectrum.isEmpty()

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

    # Signal processing ================================================
    def emitFocusChanged(self, *args):
        self.focusChanged.emit(self.currentTransition())

    def emitXUpdated(self, *args):
        """
        Update the distinct x values and send out plot data
        """
        self.distinctXUpdated.emit(self._currentSpectrum.distinctSortedX())

    def emitReadyToPlot(self, *args):
        self.readyToPlot.emit(self.generatePlotElement())

    def emitReadyToPlotX(self, *args):
        self.readyToPlotX.emit(self.generatePlotElementX())

    def emitDataUpdated(self):
        self.dataUpdated.emit(self._fullSpectra)

    def connects(self):
        # focus changed --> update plot
        self.focusChanged.connect(self.emitReadyToPlot)

        # distinct x values updated --> update plot
        self.distinctXUpdated.connect(self.emitReadyToPlotX)

        # data updated:
        self.rowsInserted.connect(self.emitDataUpdated)
        self.rowsRemoved.connect(self.emitDataUpdated)

    # Internal data manipulation methods ===============================
    def insertRow(self, row, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, row, row)
        transition = ExtrTransition()
        self._currentSpectrum.insert(row, transition)

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        self.setCurrentRow(row)

        self.endInsertRows()

        return True

    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        if self.rowCount() == 1:
            transition = ExtrTransition()
            transition.name = "Transition 1"
            self._currentSpectrum[0] = transition
            self.setCurrentRow(0)
            return True

        self.beginRemoveRows(parent, row, row)
        self._currentSpectrum.pop(row)

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        if row == self.rowCount():  # now row count is 1 less than before
            self.setCurrentRow(row - 1)
        else:
            self.setCurrentRow(row)

        self.endRemoveRows()

        return True

    # Public data manipulation =========================================
    def updateName(self, index: QModelIndex, data, role=None):
        """
        Set the data at index `index` to `data`. Note that right now
        data in the table is the name of the transition.
        """
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self._currentSpectrum[index.row()].name = data
        except (ValueError, IndexError):
            return False
        return True

    def swapXY(self):
        self._fullSpectra.swapXY()
        self.emitXUpdated()
        self.emitReadyToPlot()

    @Slot(str)
    def switchFig(self, figName: str):
        self._currentFigName = figName
        self.emitXUpdated()
        self.emitFocusChanged()
        self.layoutChanged.emit()

    @Slot()
    def removeAll(self):
        """
        Remove all rows of dataset
        """
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self._initSpectra(self.currentFigName)

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        self.setCurrentRow(0)

        self.endRemoveRows()

        self.emitXUpdated()

        return True

    @Slot(str)
    def newRow(self, str_value=None):
        rowCount = self.rowCount()

        # find a unique name for the new row
        str_value = str_value or "Transition " + str(rowCount + 1)
        counter = 1
        while str_value in self._currentSpectrum.allNames():
            str_value = "Transition " + str(rowCount + 1 + counter)
            counter += 1

        self.insertRow(rowCount)
        self.updateName(self.index(rowCount, 0), str_value, role=Qt.EditRole)

    @Slot()
    def removeCurrentRow(self):
        self.removeRow(self.currentRow)
        self.emitXUpdated()

    @Slot(ExtrTransition)
    def updateCurrentTransition(self, transition: ExtrTransition):
        """
        TODO
        Associted extracted data and tag updated from the active extracted data
        """
        self._currentSpectrum[self.currentRow] = transition
        self.emitDataUpdated()
        self.emitXUpdated()

    @Slot(int)
    def setCurrentRow(self, row: int):
        self._currentRow = row
        self.emitFocusChanged()

    def generatePlotElement(self) -> ScatterElement:
        spectra = copy(self._currentSpectrum)
        spectra.pop(self.currentRow)
        all_data = spectra.allDataConcated()

        scat_all = ScatterElement(
            "all_extractions",
            all_data[0, :],
            all_data[1, :],
            marker=r"$\times$",
            s=70,
            alpha=0.23,
        )

        return scat_all

    def generatePlotElementX(self) -> VLineElement:
        vline_data = self._currentSpectrum.distinctSortedX()
        vline = VLineElement("extraction_vlines", vline_data, alpha=0.5)

        return vline

    def registerAll(self):
        """
        Register necessary data for extracted data; these data are used to reconstruct the
        extracted data when loading a project file.
        """

        def setter(initdata):
            self._fullSpectra = initdata
            self.layoutChanged.emit()  # update the list view to show the new data
            self.emitFocusChanged()
            self.emitXUpdated()

        registry_entry = RegistryEntry(
            name="allExtractedData",
            quantity_type="r+",
            getter=lambda: self._fullSpectra,
            setter=setter,
        )
        registry = {"allExtractedData": registry_entry}

        return registry
