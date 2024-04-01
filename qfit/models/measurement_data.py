# measurement_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory eof this source tree.
############################################################################

import os
import numpy as np
from copy import copy

from typing import Dict, Tuple, Union, List, Any, Set

import skimage.morphology
import skimage.restoration
from matplotlib import colors as colors

from matplotlib.image import imread
from scipy.io import loadmat
import h5py

from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
    QAbstractListModel,
    Qt,
    QModelIndex,
)
from PySide6.QtWidgets import QFileDialog, QMessageBox

from qfit.models.data_structures import (
    PlotElement, 
    MeasMetaInfo, MeasRawXYConfig,
    NumMeasData, ImageMeasData, MeasDataType,
    FilterConfig,
)
from qfit.models.registry import Registrable, RegistryEntry
from qfit.utils.helpers import (
    OrderedDictMod,
    makeUnique,
)

class MeasFileReader:
    def fromFile(self, fileName):
        pass

    @staticmethod
    def isLikelyLabberFile(h5File):
        """
        Heuristic inspection to determine whether the h5 file might be from Labber.
        """
        if {"Data", "Instrument config", "Settings", "Step config"}.issubset(set(h5File)):
            return True
        return False

    # @staticmethod
    # def isLikelyDatapycFile(h5File):
    #     # Heuristic inspection to determine whether the h5 file might be from qfit
    #     if "__type" in h5File.attrs.keys() and h5File.attrs["__type"] == "QfitData":
    #         return True
    #     return False


class ImageFileReader(MeasFileReader):
    def fromFile(self, fileName):
        """
        Use matplotlib to read image data from file.
        """
        _, fileStr = os.path.split(fileName)
        imageData = imread(fileName)
        
        return ImageMeasData(fileStr, imageData, fileName)


class GenericH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumMeasData:
        """
        Read numerical data from h5 file. If the file is likely to be from Labber,
        use the LabberH5Reader. Otherwise, load all of the non-scalar datasets
        from the file.
        """
        with h5py.File(fileName, "r") as h5File:
            if self.isLikelyLabberFile(h5File):
                labberReader = LabberH5Reader()
                return labberReader.fromFile(fileName)
            
            # generic h5 file, attempt to read
            dataCollection = OrderedDictMod()

            def visitor_func(name, data):
                if isinstance(data, h5py.Dataset):
                    if data.shape != ():  # ignore scalar datasets
                        if data[:].dtype in [np.float32, np.float64]:
                            dataCollection[name] = data[:]

            h5File.visititems(visitor_func)

        _, fileStr = os.path.split(fileName)

        return NumMeasData(fileStr, dataCollection, fileName)


class LabberH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumMeasData:
        """
        Read numerical data from Labber h5 file. The file is assumed to have
        a specific structure, with the data stored in a dataset named "Data".
        The channel names are stored in a dataset named "Channel names".
        """
        with h5py.File(fileName, "r") as h5File:
            dataEntries = ["Data"]
            dataEntries += [name + "/Data" for name in h5File if name[0:4] == "Log_"]

            dataNames = []
            dataArrays = []
            dataCollection = OrderedDictMod()

            for entry in dataEntries:
                array = h5File[entry + "/Data"][:]
                if array.ndim != 3:
                    raise Exception(
                        "Error reading data file. Appears to be a Labber file, but its structure does not"
                        "match employed heuristics."
                    )
                dataArrays.append(array)

                names = h5File[entry + "/Channel names"][:]

                if isinstance(names[0], str):
                    dataNames.append(names)
                else:
                    newNames = []
                    for infoTuple in names:
                        newNames.append(
                            str(infoTuple[0], "utf-8")
                            + " "
                            + str(infoTuple[1], "utf-8")
                        )
                        names = newNames
                        dataNames.append(newNames)

                dataCollection[names[0] + " " + entry] = array[:, 0, 0]
                dataCollection[names[1] + " " + entry] = array[0, 1, :]
                dataCollection[names[2] + " " + entry] = array[:, 2, :]
                if len(names) == 4:
                    dataCollection[names[3] + " " + entry] = array[:, 3, :]

        _, fileStr = os.path.split(fileName)
        return NumMeasData(fileStr, dataCollection, fileName)


class MatlabReader(MeasFileReader):
    def fromFile(self, fileName) -> NumMeasData:
        """
        Read numerical data from .mat file, using scipy.io.loadmat.
        """
        dataCollection = OrderedDictMod(loadmat(fileName))
        
        _, fileStr = os.path.split(fileName)
        return NumMeasData(fileStr, dataCollection, fileName)


class CSVReader(MeasFileReader):
    def fromFile(self, fileName):
        """
        Read numerical data from .csv file, using numpy.loadtxt.
        """
        _, fileStr = os.path.split(fileName)
        return NumMeasData(
            fileStr,
            OrderedDictMod({fileName: np.loadtxt(fileName)}),
            fileName,
        )


class ListModelMeta(type(QAbstractListModel), type(Registrable)):
    pass


class MeasDataSet(QAbstractListModel, Registrable, metaclass=ListModelMeta):
    """
    Model for the list of measurement data sets. It manages the addition,
    removal, and selection of measurement data sets. It also provides
    methods for manipulating the data sets, such as 
    - select Z data, a two dimension array
    - select X and Y axis, they are one-dimension-like arrays that has 
        length compatible with Z data. Note that there may be multiple X axis 
        while only one Y axis.    
    - transpose Z. It's activated when only one X axis and one Y axis are
        selected.
    - apply filters and set the z value range.

    Parameters
    ----------
    measDatas: List[MeasurementDataType]
        list of measurement data with type NumericalMeasurementData or 
        ImageMeasurementData
    """
    # data list management
    figSwitched = Signal(str)
    metaInfoChanged = Signal(MeasMetaInfo)
    rawXYConfigChanged = Signal(MeasRawXYConfig)

    # single data processing
    readyToPlot = Signal(PlotElement)
    relimCanvas = Signal(np.ndarray, np.ndarray)
    updateRawXMap = Signal(dict)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self.fullData: List[MeasDataType] = []
        self._currentRow: int = 0

        self.checkedRawX: List[str] = []
        self.checkedRawY: List[str] = []

    # init & load data list ============================================
    @staticmethod
    def _rawDataFromFile(fileName) -> MeasDataType | None:
        """
        Read experimental data from file. It supports .h5, .mat, .csv, .jpg, 
        .jpeg, .png files.

        Parameters
        ----------
        fileName: str
            Name of file to be read.

        Returns
        -------
        MeasurementDataType
            The data read from the file.
        """
        _, suffix = os.path.splitext(fileName)

        if suffix.lower() in (".h5", ".hdf5"):
            reader = GenericH5Reader()
        elif suffix.lower() in (".jpg", ".jpeg", ".png"):
            reader = ImageFileReader()
        elif suffix.lower() == ".mat":
            reader = MatlabReader()
        elif suffix.lower() == ".csv":
            reader = CSVReader()
        else:
            return None
        
        try:
            data = reader.fromFile(fileName)
        except ValueError:
            # can't identify the relavant measurement data
            return None
        
        return data
    
    def _measDataFromDialog(
        self, 
        home: str | None = None,
        multiple: bool = True,
    ) -> List["MeasDataType"] | None:
        """
        Open a dialog to select a file, and then read the measurement data from 
        the file. It will keep asking for files until a valid file is selected.
        Only break the loop when the user selects a valid file or cancels the
        dialog.

        Parameters
        ----------
        home : str
            the home directory to start the dialog
        multiple : bool
            whether to allow multiple files to be selected

        Returns
        -------
        List[MeasurementDataType] | None
            The data read from the file. If the user canceled the dialog, 
            return None.
        """
        # configure the file dialog
        if home is None:
            home = os.path.expanduser("~")
        fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"

        while True:
            # start a loop of asking for files, only break the loop
            # when the user selects a valid file
            if multiple:
                fileNames, _ = QFileDialog.getOpenFileNames(
                    self.parent(), "Open", home, fileCategories
                )
            else:
                fileName, _ = QFileDialog.getOpenFileName(
                    self.parent(), "Open", home, fileCategories
                )
                fileNames = [fileName]

            if not fileNames:
                # user canceled the dialog
                return None

            measurementData = []
            for fileName in fileNames:
                measData = self._rawDataFromFile(fileName)

                if measData is None:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Error opening file.")
                    msg.setInformativeText(
                        "The selected file format is supported, but heuristic inspection "
                        "failed to identify suitable data inside the file."
                    )
                    msg.setWindowTitle("Error")
                    _ = msg.exec_()
                    break  # break the loop and ask for files again
                else:
                    measurementData.append(measData)

            if len(measurementData) == len(fileNames):
                break       # break the loop if all files are successfully read

        return measurementData
    
    def loadData(
        self,
        fileName: str | List[str] | None = None,
    ) -> bool:
        """
        Load the data from the file using the file name. If the file name is
        not provided, open a dialog to select a file. 

        Parameters
        ----------
        fileName: str | List[str] | None
            The name of the file to be loaded. If None, open a dialog to select
            a file. If a string or a list of strings, load the file with the 
            file names. Inside the GUI, the user always uses a dialog.

        Returns
        -------
        bool
            False if user canceled the dialog, True otherwise. 

        """
        if fileName is not None:
            if isinstance(fileName, str):
                if not os.path.isfile(fileName):
                    # TODO: show an error in the GUI instead of raising an error
                    raise FileNotFoundError(f"File '{fileName}' does not exist.")
                    return True     # continue opening the gui, while data is not loaded
            elif isinstance(fileName, list):
                for file in fileName:
                    if not os.path.isfile(file):
                    # TODO: show an error in the GUI instead of raising an error
                        raise FileNotFoundError(f"File '{file}' does not exist.")
                        return True
            else:
                # TODO: show an error in the GUI instead of raising an error
                raise ValueError("measurementFileName must be a string or a list of strings.")
                return True

        # read measurement files from dialog
        if fileName is None:
            measurementData = self._measDataFromDialog()
            if measurementData is None:
                # user canceled the dialog, return False to close the GUI
                return False
            
        # read measurement files from a single file name
        elif isinstance(fileName, str):
            data = self._rawDataFromFile(fileName)
            if data is None:
                # TODO: show an error in the GUI instead of raising an error
                raise FileNotFoundError(f"Can't load file '{fileName}'.")
                return True
            measurementData = [data]
        
        # read measurement files from a list of file names
        else:
            measurementData = []
            for file in fileName:
                measData = self._rawDataFromFile(file)
                if measData is None:
                    # TODO: show an error in the GUI instead of raising an error
                    raise FileNotFoundError(f"Can't load file '{file}'.")
                    return True
                measurementData.append(measData)

        # add the measurement data to the list
        self.fullData = self.fullData + measurementData

        # rename the measurement data with repeated names
        names = [measData.name for measData in self.fullData]
        uniqueNames = makeUnique(names)
        for measData, name in zip(self.fullData, uniqueNames):
            measData.name = name

        # if there are new data loaded, emit the signals
        if measurementData != []:
            self.emitMetaInfo()
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()
            self.emitFigSwitched()

        # update the raw X and Y axis names
        if measurementData != []:
            self._clearRawXY()
            self.emitRawXYConfig()

        return True

    def removeDataFile(self, index: int) -> None:
        """
        Remove a data file from the list of files to be loaded.

        Parameters
        ----------
        index: int
            Index of the file to be removed.
        """
        self.fullData.pop(index)

        # if the current row is removed, set the current row to the first row
        if self._currentRow >= len(self.fullData):
            self._currentRow = 0

        self.emitMetaInfo()
        self.emitRawXYConfig()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitFigSwitched()

    # Qt view related ==================================================        
    @property
    def figNames(self) -> List[str]:
        return [data.name for data in self.fullData]
    
    @property
    def currentRow(self) -> int:
        return self._currentRow

    @property
    def currentMeasData(self) -> "MeasDataType":
        return self.fullData[self._currentRow]
    
    @property
    def currentFigName(self) -> str:
        return self.currentMeasData.name

    def data(self, index: QModelIndex, role):
        """
        The NAME & Icon of the measurement data set!
        """
        if role == Qt.DisplayRole:
            str_value = self.fullData[index.row()].name
            return str_value

    def rowCount(self, *args) -> int:
        return len(self.fullData)

    def isEmpty(self) -> bool:
        return self.fullData == []

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags
    
    def insertRow(self):
        """
        Insert a new row at the end of the table.
        """
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)

        result = self.loadData()
        if not result:
            return False

        # update the current row before emitting the rowsInserted signal
        # (which will be emitted by endInsertRows)
        self.switchFig(-1)

        self.endInsertRows()

        return True

    def removeRow(self):
        """
        Remove a row from the table.
        """
        if self.rowCount() == 0:
            return False
        
        row = self.currentRow

        self.beginRemoveRows(QModelIndex(), row, row)
        self.fullData.pop(row)

        # update the current row before emitting the rowsRemoved signal
        # (which will be emitted by endRemoveRows)
        if self.rowCount() == 0:
            self._currentRow = 0
        elif row == self.rowCount():  # now row count is 1 less than before
            self.switchFig(row - 1)
        else:
            self.switchFig(row)

        self.endRemoveRows()

        return True

    # Raw XY management ================================================
    @classmethod
    def isSubsetExclusively(
        cls,
        checkedAxes: List[str] | Set[str],
        candidates: List[str] | Set[str],
        otherCandidates: List[str] | Set[str],
    ) -> bool:
        """
        Return True if the currently checked raw axes are exclusively 
        conpatible with the candidates (not compatible with the other axes).

        Parameters
        ----------
        checkedAxes: List[str]
            The names of the currently checked raw axes.
        candidates: List[str]
            The candidates for the corresponding axis.
        otherCandidates: List[str]
            The candidates for the other axis.

        Return 
        ------
        bool
            True if the currently checked raw axes are exclusively 
            conpatible with the candidates (not compatible with the other axes).
        """
        if len(checkedAxes) == 0:
            return False
        
        checkedSet = set(checkedAxes)
        return (
            checkedSet.issubset(candidates)
            and not checkedSet.issubset(otherCandidates)
        )

    @property
    def xCandidates(self) -> List[str]:
        """
        Get the raw X candidates from all data files. Currently, we show all
        of the X and Y axis candidates from all data files, and let the user
        select the X names. 

        Returns
        -------
        List[str]
            The candidates for raw X axis names.
        """
        if not self.fullData:
            return []
        
        candidates = [
            set(data.xCandidates.keyList + data.yCandidates.keyList) 
            for data in self.fullData
        ]
        candidates = set.intersection(*candidates)

        return list(candidates)
    
    @property
    def yCandidates(self) -> List[str]:
        """
        Get the raw Y candidates from all data files. Currently, we show all
        of the X and Y axis candidates from all data files, and let the user
        select the Y name -- the same as the X names.

        Returns
        -------
        List[str]
            The candidates for raw Y axis names -- the same as the X names.
        """
        return self.xCandidates
    
    @property
    def grayedRawX(self) -> List[str]:
        """
        Some of the raw X & raw Y configurations are not allowed, so we need to
        forbid the user to select invalid configurations by graying out some
        of the names.

        For X axes, we should gray out:
        - the names that are checked for Y axis
        - the names that are not compatible with the current selected X axis 
            names.
        """
        checkedX = set(self.checkedRawX)
        checkedY = set(self.checkedRawY)

        # we will calculate a maximum set of grayed out X axis names, which
        # may contain the names that are not in X candidates:

        # the names that are checked for Y axis
        grayedX = set(self.checkedRawY)

        for data in self.fullData:
            xCompatible = set(data.xCandidates.keyList)
            yCompatible = set(data.yCandidates.keyList)

            # the names that are not compatible with the current selected X axis
            if self.isSubsetExclusively(checkedX, xCompatible, yCompatible):
                grayedX = grayedX.union(yCompatible)

            # the names that are only compatible with the current selected Y axis
            if self.isSubsetExclusively(checkedY, yCompatible, xCompatible):
                grayedX = grayedX.union(yCompatible)

        return list(grayedX)

    @property
    def grayedRawY(self) -> List[str]:
        """
        Some of the raw X & raw Y configurations are not allowed, so we need to
        forbid the user to select invalid configurations by graying out some
        of the names.

        For Y axes, we should gray out:
        - the names that are checked for X axis
        - the rest of the names, if the user has checked a name 
        """
        checkedX = set(self.checkedRawX)

        # the names that are checked for X axis
        grayedY = set(self.checkedRawX)

        # the rest of names that are not checked for Y axis
        if len(self.checkedRawY) == 1:
            remainingCand = copy(self.yCandidates)
            remainingCand.remove(self.checkedRawY[0])
        else:
            remainingCand = []
        grayedY = grayedY.union(set(remainingCand))

        for data in self.fullData:
            xCompatible = set(data.xCandidates.keyList)
            yCompatible = set(data.yCandidates.keyList)

            # the names that are not compatible with the current selected X axis
            if self.isSubsetExclusively(checkedX, xCompatible, yCompatible):
                grayedY = grayedY.union(xCompatible)

        grayedY = grayedY.intersection(self.yCandidates)

        return list(grayedY)

    def _clearRawXY(self) -> None:
        """
        Initialize (clear) the raw X and Y axis names.
        """
        self.checkedRawX = []
        self.checkedRawY = []
        self.emitRawXYConfig()
    
    def _setRawXY(self, xNames: List[str], yNames: List[str]) -> None:
        """
        Set the raw X and Y axis names without sending any signals.

        Parameters
        ----------
        xNames: List[str]
            The raw X axis names.
        yNames: List[str]
            A one-element list of the raw Y axis name.
        """
        # the validity check should be done outside of this method
        self.checkedRawX = xNames
        self.checkedRawY = yNames

        if self._rawXYIsValid():
            for data in self.fullData:
                data.setRawXY(self.checkedRawX, self.checkedRawY)

    def _rawXYIsValid(self) -> bool:
        """
        Check if the selected raw X and Y axis names are valid. The raw X and
        Y axis names should be checked, and the user should select one X axis
        and one Y axis.

        Returns
        -------
        bool
            True if the raw X and Y axis names are valid, False otherwise.
        """
        xNames = set(self.checkedRawX)
        yNames = set(self.checkedRawY)

        # length
        if len(xNames) == 0 or len(yNames) != 1:
            return False

        # compatibility
        if not xNames.issubset(self.xCandidates):
            return False
        if not yNames.issubset(self.yCandidates):
            return False
        if len(xNames.intersection(self.grayedRawX)) > 0:
            return False
        if len(yNames.intersection(self.grayedRawY)) > 0:
            return False
        
        return True

    # Data list signals & slots ========================================
    @Slot(str)
    def switchFig(self, fig: str | int):
        """
        Switch the current measurement data by the name, and emit the
        readyToPlot, relimCanvas, and updateRawXMap signals.
        """
        if isinstance(fig, int):
            self._currentRow = fig
        else:
            for i, data in enumerate(self.fullData):
                if data.name == fig:
                    self._currentRow = i
                    break
        
        self.emitMetaInfo()
        self.emitRawXYConfig()      # update transpose button 
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()
        self.emitFigSwitched()

    def emitMetaInfo(self):
        self.metaInfoChanged.emit(self.currentMeasData.generateMetaInfo())

    def emitFigSwitched(self):
        self.figSwitched.emit(self.currentFigName) 

    def exportRawXYConfig(self) -> MeasRawXYConfig:
        """
        Export the raw X and Y axis names to view.

        Returns
        -------
        MeasRawXYConfig
            The configuration of raw X and Y axis names, including all of the 
            candidates, selected X and Y axis names, and the names to be 
            grayed out.
        """
        return MeasRawXYConfig(
            checkedX = self.checkedRawX, 
            checkedY = self.checkedRawY,
            xCandidates = self.xCandidates,
            yCandidates = self.yCandidates,
            grayedX = self.grayedRawX,
            grayedY = self.grayedRawY,
            allowTranspose = self.currentMeasData.ambiguousZOrient,
            allowContinue = self._rawXYIsValid() and len(self.fullData) > 0,
        )
    
    @Slot()
    def storeRawXYConfig(self, rawXYConfig: MeasRawXYConfig) -> None:
        """
        Store the raw X and Y axis names from view. There are a few cases
        to consider:
        - If the user has checked a name for X (Y), and this axis is actually
            corresponding Y axis in some data, swap the X and Y axis names for
            those data files and transpose Z.
        """
        # swap the X and Y axis names if necessary
        # note that it will re-init the stored raw XY info 
        checkedX = rawXYConfig.checkedX
        checkedY = rawXYConfig.checkedY
        for data in self.fullData:
            swap = False
            if self.isSubsetExclusively(
                checkedX, 
                data.yCandidates.keyList, 
                data.xCandidates.keyList
            ):
                swap = True
            if self.isSubsetExclusively(
                checkedY, 
                data.xCandidates.keyList, 
                data.yCandidates.keyList
            ):
                swap = True 
            
            if swap:
                data.swapXY()
                if data is self.currentMeasData:
                    self.emitMetaInfo()
        
        # store the raw X and Y axis names
        self._setRawXY(checkedX, checkedY)

        # gray out the X and Y axis names
        self.emitRawXYConfig()

        if self._rawXYIsValid():
            # update view
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()
        else:
            # some warning message?
            pass 

    def emitRawXYConfig(self):
        self.rawXYConfigChanged.emit(self.exportRawXYConfig())

    # Single data signal & slots =======================================
    def emitReadyToPlot(self):
        """
        Emit the readyToPlot signal with the current plotting element.
        """
        self.readyToPlot.emit(self.currentMeasData.generatePlotElement())
    
    def emitRelimCanvas(self):
        """
        Emit the relimCanvas signal with the current x and y axis data,
        which will be used to relim the canvas, set x snap values.
        """
        self.relimCanvas.emit(
            self.currentMeasData.principalX.data,
            self.currentMeasData.principalY.data,
        )

    def emitRawXMap(self):
        """
        Emit the updateRawXMap signal with the raw x values corresponding
        to the current x values.
        """
        self.updateRawXMap.emit({
            data.name: data.rawXByPrincipalX for data in self.fullData
        })

    @Slot(FilterConfig)
    def storeFilter(self, filterConfig: FilterConfig):
        """
        Store the filter configuration, and emit the readyToPlot signal.
        """
        self.currentMeasData.setFilter(filterConfig)
        self.emitReadyToPlot()

    def exportFilter(self) -> FilterConfig:
        """
        Export the filter configuration to view.

        Returns
        -------
        FilterConfig
            The filter configuration.
        """
        return self.currentMeasData.getFilter()

    @Slot(int)
    def storePrincipalZ(self, itemIndex: int):
        """
        Set the current measurement data, and emit the readyToPlot signal, 
        and relimCanvas signal.
        """
        self.currentMeasData.setPrincipalZ(itemIndex)
        self.emitReadyToPlot()
        self.emitRelimCanvas()

    @Slot()
    def swapXY(self):
        """
        Swap the x and y axes, and emit the readyToPlot, relimCanvas, and
        updateRawXMap signals.
        """
        self.currentMeasData.swapXY()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

    @Slot()
    def transposeZ(self):
        """
        Transpose the z axis, and emit the readyToPlot signal.
        """
        self.currentMeasData.transposeZ()
        self.emitReadyToPlot()
        self.emitRelimCanvas()
        self.emitRawXMap()

    # registry =========================================================
    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all of the measurement data.
        """

        def dataSetter(value):
            self.fullData = value
            self.emitReadyToPlot()
            self.emitRelimCanvas()
            self.emitRawXMap()

        return {
            "measDataSet.currentRow": RegistryEntry(
                name="measDataSet.currentRow",
                quantity_type="r+",
                getter=lambda: self._currentRow,
                setter=lambda value: setattr(self, "_currentRow", value),
            ),
            "measDataSet.data": RegistryEntry(
                name="measDataSet.data",
                quantity_type="r+",
                getter=lambda: self.fullData,
                setter=dataSetter,
            ),
        }
