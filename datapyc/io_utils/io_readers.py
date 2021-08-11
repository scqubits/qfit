# io_readers.py
#
# This file is part of datapyc.
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

import datapyc.io_utils.file_io as io
import datapyc.io_utils.file_io_backends as io_backends

from datapyc.core.helpers import (
    OrderedDictMod,
    hasIdenticalCols,
    hasIdenticalRows,
    isValid2dArray,
)
from datapyc.data.measurement_data import ImageMeasurementData, NumericalMeasurementData


def readFileData(fileName):
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
    measurementData = reader.fromFile(fileName)
    return measurementData


class ImageFileReader:
    def fromFile(self, fileName):
        _, fileStr = os.path.split(fileName)
        try:
            imageData = imread(fileName)
        except OSError:
            return None
        return ImageMeasurementData(fileStr, imageData)


class GenericH5Reader:
    def fromFile(self, fileName):
        with h5py.File(fileName, "r") as h5File:
            if isLikelyLabberFile(h5File):
                labberReader = LabberH5Reader()
                return labberReader.fromFile(fileName)

            if isLikelyDatapycFile(h5File):
                datapycReader = io_backends.H5Reader(fileName)
                iodata = datapycReader.from_file(fileName)
                return io.deserialize(iodata)

            # generic h5 file, attempt to read
            dataCollection = {}

            def visitor_func(name, data):
                if isinstance(data, h5py.Dataset) and data[:].dtype in [
                    np.float32,
                    np.float64,
                ]:
                    dataCollection[name] = data[:]

            h5File.visititems(visitor_func)

        zCandidates = findZData(dataCollection)
        if not zCandidates:
            return None
        return NumericalMeasurementData(dataCollection, zCandidates)


class LabberH5Reader:
    def fromFile(self, fileName):

        with h5py.File(fileName, "r") as h5File:
            dataEntries = ["Data"]
            dataEntries += [name + "/Data" for name in h5File if name[0:4] == "Log_"]

            dataNames = []
            dataArrays = []
            dataCollection = {}

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
                        newNames.append(str(infoTuple[0]) + " " + str(infoTuple[1]))
                        names = newNames
                        dataNames.append(newNames)

                dataCollection[names[0] + " " + entry] = array[:, 0, 0]
                dataCollection[names[1] + " " + entry] = array[0, 1, :]
                dataCollection[names[2] + " " + entry] = array[:, 2, :]
                if len(names) == 4:
                    dataCollection[names[3] + " " + entry] = array[:, 3, :]

        zCandidates = findZData(dataCollection)
        if not zCandidates:
            return None
        return NumericalMeasurementData(dataCollection, zCandidates)


class MatlabReader:
    def fromFile(self, fileName):
        dataCollection = loadmat(fileName)
        zCandidates = findZData(dataCollection)
        if not zCandidates:
            return None
        return NumericalMeasurementData(dataCollection, zCandidates)


class CSVReader:
    def fromFile(self, fileName):
        return NumericalMeasurementData({fileName: np.loadtxt(fileName)})


def isLikelyLabberFile(h5File):
    # Heuristic inspection to determine whether the h5 file might be from Labber
    if {"Data", "Instrument config", "Settings", "Step config"}.issubset(set(h5File)):
        return True
    return False


def isLikelyDatapycFile(h5File):
    # Heuristic inspection to determine whether the h5 file might be from datapyc
    if "__type" in h5File.attrs.keys() and h5File.attrs["__type"] == "DatapycData":
        return True
    return False


def findZData(rawData):
    zCandidates = OrderedDictMod()
    for name, theObject in rawData.items():
        if isinstance(theObject, np.ndarray) and isValid2dArray(theObject):
            if not (hasIdenticalCols(theObject) or hasIdenticalRows(theObject)):
                zCandidates[name] = theObject
    return zCandidates
