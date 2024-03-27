import numpy as np
import os
import h5py

from matplotlib.image import imread
from scipy.io import loadmat

from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from qfit.utils.helpers import (
    DictItem,
    OrderedDictMod,
    hasIdenticalCols,
    hasIdenticalRows,
    isValid1dArray,
    isValid2dArray,
    makeUnique,
)

from qfit.models.measurement_data import (
    ImageMeasurementData, NumericalMeasurementData, MeasurementDataType
)
from qfit.models.registry import Registrable

from typing import Dict, Tuple, Union, List, Optional


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
        
        return ImageMeasurementData(fileStr, imageData, fileName)


class GenericH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
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

        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class LabberH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
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
        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class MatlabReader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
        """
        Read numerical data from .mat file, using scipy.io.loadmat.
        """
        dataCollection = OrderedDictMod(loadmat(fileName))
        
        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(fileStr, dataCollection, fileName)


class CSVReader(MeasFileReader):
    def fromFile(self, fileName):
        """
        Read numerical data from .csv file, using numpy.loadtxt.
        """
        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(
            fileStr,
            OrderedDictMod({fileName: np.loadtxt(fileName)}),
            fileName,
        )


class CombinedMeta(type(QObject), type(Registrable)):
    pass

class MeasDataImporter(QObject, Registrable, metaclass=CombinedMeta):
    """
    A class to load multiple data files. It is connected to a ListView in the 
    GUI, which displays the list of data files to be loaded. The user can add 
    or remove files from the list. 
    Users can process these data, including 
    - select Z data, a two dimension array
    - select X and Y axis, they are one-dimension-like arrays that has 
        length compatible with Z data. Note that there may be multiple X axis 
        while only one Y axis.    
    - transpose Z. It's activated when only one X axis and one Y axis are
        selected.
    """
    figSwitched = Signal(str)
    def __init__(
        self, 
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._data: List[MeasurementDataType] = []

        self._xCandidateNames: List[str] = []
        self._yCandidateNames: List[str] = []
        self._xNames: List[str] = []
        self._yNames: List[str] = []

    # read ==============================================================
    @staticmethod
    def _rawDataFromFile(fileName) -> MeasurementDataType:
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
            raise Exception("IOError: The requested file type is not supported.")
        data = reader.fromFile(fileName)
        return data
    
    def _measDataFromDialog(
        self, 
        home: str | None = None,
        multiple: bool = True,
    ) -> List["MeasurementDataType"] | None:
        """
        Open a dialog to select a file, then read the measurement data from the file.

        Parameters
        ----------
        home : str
            the home directory to start the dialog
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
    
    def loadMultiData(
        self, 
        measurementFileName: str | List[str] | None = None,
    ) -> List[MeasurementDataType] | None:
        """
        Open a dialog to select a measurement file, then create a new project.
        It is a slot for the new project button in the menu.

        Note: At the moment, this method should only be called at the beginning 
        of the app.

        Parameters
        ----------
        measurementFileName : str | List[str] | None
            The names of the files to be loaded. If None, open a dialog to select
            a file. If a string or a list of strings, load the file with the 
            file names. 

        Returns
        -------
        List[MeasurementDataType] | None
            A list o the measurement data read from the file. None if the dialog
            is canceled.
        """
        if measurementFileName is not None:
            if isinstance(measurementFileName, str):
                if not os.path.isfile(measurementFileName):
                    raise FileNotFoundError(f"File '{measurementFileName}' does not exist.")
            elif isinstance(measurementFileName, list):
                for file in measurementFileName:
                    if not os.path.isfile(file):
                        raise FileNotFoundError(f"File '{file}' does not exist.")
            else:
                raise ValueError("measurementFileName must be a string or a list of strings.")

        # read measurement files from dialog
        if measurementFileName is None:
            measurementData = self._measDataFromDialog()
            if measurementData is None:
                # user canceled the dialog
                return None
            
        # read measurement files from a single file name
        elif isinstance(measurementFileName, str):
            measurementData = [self._rawDataFromFile(measurementFileName)]
            if measurementData[0] is None:
                raise FileNotFoundError(f"Can't load file '{measurementFileName}'.")
        
        # read measurement files from a list of file names
        else:
            measurementData = []
            for file in measurementFileName:
                measData = self._rawDataFromFile(file)
                if measData is None:
                    raise FileNotFoundError(f"Can't load file '{file}'.")
                measurementData.append(measData)

        # rename the measurement data with repeated names
        names = [measData.name for measData in measurementData]
        uniqueNames = makeUnique(names)
        for measData, name in zip(measurementData, uniqueNames):
            measData.name = name

        return measurementData
    
    def loadData(self, fileName: str) -> None:
        """
        Add a data file to the list of files to be loaded. Check if the file
        has X and Y axis names. If not, refresh _compatibleXNames and
        _compatibleYNames and clear the list of _xNames and _yNames, so that
        user have to select X and Y axis names again.

        Parameters
        ----------
        fileName: str
            Name of the file to be loaded.
        """
        raise NotImplementedError

    def removeDataFile(self, index: int) -> None:
        """
        Remove a data file from the list of files to be loaded.

        Parameters
        ----------
        index: int
            Index of the file to be removed.
        """
        raise NotImplementedError

    # process ==========================================================
    @Slot(str)
    def switchFig(self, figName: str) -> None:
        """
        Switch the figure to be displayed.

        Parameters
        ----------
        figName: str
            Name of the figure to be displayed.
        """
        raise NotImplementedError
    
        self.figSwitched.emit(figName)
