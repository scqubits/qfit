# io_readers.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import os

import h5py
import numpy as np

from matplotlib.image import imread
from scipy.io import loadmat

from qfit.utils.helpers import (
    OrderedDictMod,
)
from qfit.models.measurement_data import (
    ImageMeasurementData, NumericalMeasurementData, MeasurementDataType)


def readMeasurementFile(fileName) -> MeasurementDataType:
    """
    Read experimental data from file.

    Parameters
    ----------
    fileName: str
        Name of file to be read.

    Returns
    -------
    Serializable
        class instance initialized with the data from the file
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


class MeasFileReader:
    def fromFile(self, fileName):
        pass

    @staticmethod
    def isLikelyLabberFile(h5File):
        # Heuristic inspection to determine whether the h5 file might be from Labber
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
        _, fileStr = os.path.split(fileName)
        imageData = imread(fileName)
        
        return ImageMeasurementData(fileStr, imageData)


class GenericH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
        with h5py.File(fileName, "r") as h5File:
            if self.isLikelyLabberFile(h5File):
                labberReader = LabberH5Reader()
                return labberReader.fromFile(fileName)
            
            # generic h5 file, attempt to read
            dataCollection = OrderedDictMod()

            def visitor_func(name, data):
                if isinstance(data, h5py.Dataset) and data[:].dtype in [
                    np.float32,
                    np.float64,
                ]:
                    dataCollection[name] = data[:]

            h5File.visititems(visitor_func)

        _, fileStr = os.path.split(fileName)

        return NumericalMeasurementData(fileStr, dataCollection)


class LabberH5Reader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
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
        return NumericalMeasurementData(fileStr, dataCollection)


class MatlabReader(MeasFileReader):
    def fromFile(self, fileName) -> NumericalMeasurementData:
        dataCollection = loadmat(fileName)
        
        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(fileStr, dataCollection)


class CSVReader(MeasFileReader):
    def fromFile(self, fileName):
        _, fileStr = os.path.split(fileName)
        return NumericalMeasurementData(
            fileStr,
            {fileName: np.loadtxt(fileName)}
        )