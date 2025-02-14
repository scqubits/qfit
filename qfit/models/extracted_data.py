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
    QModelIndex,
    Qt,
    Slot,
    Signal,
    QObject,
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
from qfit.settings import MARKER_SIZE

from copy import deepcopy, copy

if TYPE_CHECKING:
    from qfit.utils.helpers import OrderedDictMod


class ActiveExtractedData(QObject):
    """
    This class holds one extracted transition, as a series of markers on 
    the canvas. User can add, remove, and replace the data points, and 
    the view will change correspondingly.

    Parameters
    ----------
    parent: QObject
        The parent QObject of this model.
    """
    dataUpdated = Signal(ExtrTransition)    # when user add or remove data points
    dataSwitched = Signal(ExtrTransition)   # when user select and focus on a new row
    readyToPlot = Signal(
        ScatterElement
    )  # send the plot element to the mpl canvas

    def __init__(self, parent):
        super().__init__(parent)

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
        Replaces the current table of extracted data points with a new 
        dataset of points. It's used when user clicks on a new row in the
        list view.

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
        """
        Generate a plot element and send it to the mpl canvas through the
        readyToPlot signal. For the active extracted data, it's a scatter
        plot of the data points with a larger marker.
        """
        # tag mode
        scat_active = ScatterElement(
            "active_extractions",
            self._transition.data[0],
            self._transition.data[1],
            marker=r"$\odot$",
            s = MARKER_SIZE,
            alpha = 0.3,
            zorder = 1,
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
    """
    This class holds all extracted transitions for all figures, and each
    figure has a list of transitions. User can add, remove, and replace
    the transitions, and the view will change correspondingly.

    Parameters
    ----------
    parent: QObject
        The parent QObject of this model.
    """

    dataUpdated = Signal(FullExtr)  # when user add or remove data points
    focusChanged = Signal(ExtrTransition)  # when user select and focus on a new row
    readyToPlot = Signal(ScatterElement)  # send the plot element to the mpl canvas

    distinctXUpdated = Signal(np.ndarray)  # when user extract (remove) data points
    readyToPlotX = Signal(VLineElement)  # connected to the above signal

    _figNames: List[str]
    _currentFigName: str
    _currentRow: int

    def __init__(self, parent):
        super().__init__(parent)

        self._figNames = []
        self._fullSpectra = FullExtr()
        self._currentRow = 0

        self._signalProcessing()

    def replaceMeasData(
        self,
        figNames: List[str],
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.

        Parameters
        ----------
        figNames: List[str]
            The names of the figures.
        """
        self._figNames = figNames

    def dynamicalInit(self,):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.
        """
        if self._figNames == []:
            raise AttributeError("Should call updateMeasData before dynamicalInit")

        self._initFullSpectra()

        self._currentFigName = self._figNames[0]

    def _initFullSpectra(self):
        """
        Initialize the FullExtr for all figures.
        """
        for name in self._figNames:
            self._initSpectra(name)

    def _initSpectra(self, figName: str):
        """
        Initialize a new spectra (list of transitions) for a new figure.
        """
        transition = ExtrTransition()
        transition.name = "Transition 1"
        spectra = ExtrSpectra(
            transition,
        )
        self._fullSpectra[figName] = spectra

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
            if self._currentSpectrum[index.row()].tag.tagType != "NO_TAG":
                # icon1.addPixmap(
                #     QtGui.QPixmap(":/icons/svg/tag.svg").scaled(40, 40),
                #     QtGui.QIcon.Normal,
                #     QtGui.QIcon.Off,
                # )
                icon1 = QtGui.QIcon(":/icons/svg/tag.svg")
            else:
                # icon1.addPixmap(
                #     QtGui.QPixmap(":/icons/svg/tag-question.svg").scaled(40, 40),
                #     QtGui.QIcon.Normal,
                #     QtGui.QIcon.Off,
                # )
                icon1 = QtGui.QIcon(":/icons/svg/tag-question.svg")
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
        """
        Emit focusChanged signal with the current transition, indicating

        """
        self.focusChanged.emit(self.currentTransition())

    def emitXUpdated(self, *args):
        """
        Update the distinct x values and send out plot data
        """
        self.distinctXUpdated.emit(self._currentSpectrum.distinctSortedX())

    def emitReadyToPlot(self, *args):
        """
        Emit readyToPlot signal with the plot element
        """
        self.readyToPlot.emit(self.generatePlotElement())

    def emitReadyToPlotX(self, *args):
        """
        Emit readyToPlotX signal with the plot element
        """
        self.readyToPlotX.emit(self.generatePlotElementX())

    def emitDataUpdated(self):
        """
        Emit dataUpdated signal with the current full spectra
        """
        self.dataUpdated.emit(self._fullSpectra)

    def _signalProcessing(self):
        # focus changed --> update plot
        self.focusChanged.connect(self.emitReadyToPlot)

        # distinct x values updated --> update plot
        self.distinctXUpdated.connect(self.emitReadyToPlotX)

        # data updated:
        self.rowsInserted.connect(self.emitDataUpdated)
        self.rowsRemoved.connect(self.emitDataUpdated)

    # Internal data manipulation methods ===============================
    def insertRow(self, row, parent=QModelIndex(), *args, **kwargs):
        """
        Insert a new row at the end of the table.
        """
        self.beginInsertRows(parent, row, row)
        transition = ExtrTransition()
        self._currentSpectrum.insert(row, transition)

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        self.setCurrentRow(row)

        self.endInsertRows()

        return True

    def removeRow(self, row, parent=QModelIndex(), *args, **kwargs):
        """
        Remove a row from the table.
        """
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
    def setData(self, index: QModelIndex, data, role=None):
        """
        Override Qt's native setData method to update the name of the transition.
        
        Update:
        1. The name shown in the list view
        2. The name of the currently selected spectrum
        """
        if not (index.isValid() and role == Qt.EditRole):
            return False
        try:
            self._currentSpectrum[index.row()].name = data
        except (ValueError, IndexError):
            return False
        return True

    def swapXY(self):
        """
        Swap the x and y values of the current transition.
        """
        self._fullSpectra.swapXY()
        self.emitXUpdated()
        self.emitReadyToPlot()

    @Slot(str)
    def switchFig(self, figName: str):
        """
        Switch to a new figure.
        """
        if figName not in self._figNames:
            # this happens in the data importing stage, where the model is 
            # not fully initialized by the measurement data
            return 

        self._currentFigName = figName
        self.emitXUpdated()
        self.emitDataUpdated()
        self.setCurrentRow(0)
        self.layoutChanged.emit() # update the list view to show the new data

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
        """
        Add a new row to the table with name `transition_x`
        """
        rowCount = self.rowCount()

        # find a unique name for the new row
        str_value = str_value or "Transition " + str(rowCount + 1)
        counter = 1
        while str_value in self._currentSpectrum.allNames():
            str_value = "Transition " + str(rowCount + 1 + counter)
            counter += 1

        self.insertRow(rowCount)
        self.setData(self.index(rowCount, 0), str_value, role=Qt.EditRole)

    @Slot()
    def removeCurrentRow(self):
        """
        Remove the current row from the table and emit the xUpdated signal.
        """
        self.removeRow(self.currentRow)
        self.emitXUpdated()

    @Slot(ExtrTransition)
    def updateCurrentTransition(self, transition: ExtrTransition):
        """
        Update the current transition with a new transition, and emit the
        dataUpdated and xUpdated signals.
        """
        self._currentSpectrum[self.currentRow] = transition
        self.emitDataUpdated()
        self.emitXUpdated()

    @Slot(int)
    def setCurrentRow(self, row: int):
        """
        Set the current row and emit the focusChanged signal.
        """
        self._currentRow = row
        self.emitFocusChanged()

    def generatePlotElement(self) -> ScatterElement:
        """
        Generate a plot element and send it to the mpl canvas through the
        readyToPlot signal. For the inactive extracted data, it's a scatter
        plot of the data points with a "x" marker.
        """
        spectra = copy(self._currentSpectrum)
        spectra.pop(self.currentRow)
        all_data = spectra.allDataConcated()

        scat_all = ScatterElement(
            "all_extractions",
            all_data[0, :],
            all_data[1, :],
            marker = r"$\times$",
            s = 70,
            alpha = 0.23,
            zorder = 1,
        )

        return scat_all

    def generatePlotElementX(self) -> VLineElement:
        """
        Generate a plot element representing the distinct x coordinates
        of the current spectra, and send it to the mpl canvas through the
        readyToPlotX signal.  
        """
        vline_data = self._currentSpectrum.distinctSortedX()
        vline = VLineElement(
            "extraction_vlines", 
            vline_data, 
            alpha = 0.5,
            zorder = 1,
        )

        return vline

    def registerAll(self):
        """
        Register the fullSpectra data to the registry.
        """

        def setter(initdata):
            self._fullSpectra = initdata
            self.layoutChanged.emit()  # update the list view to show the new data
            self.emitFocusChanged()
            self.emitDataUpdated()
            self.emitXUpdated()

        registry_entry = RegistryEntry(
            name="allExtractedData",
            quantity_type="r+",
            getter=lambda: self._fullSpectra,
            setter=setter,
        )
        registry = {"allExtractedData": registry_entry}

        return registry
