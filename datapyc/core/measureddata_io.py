# measureddata_io.py
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

from datapyc.core.measureddata_models import NumericalMeasurementData, ImageMeasurementData


def readMeasurementData(fileName):
    """
    Read experimental data from file.

    Parameters
    ----------
    fileName: str
        Name of file to be read.
    fileHandle: h5py.Group, optional
        Specify Group inside h5 file if only this subgroup should be read.

    Returns
    -------
    Serializable
        class instance initialized with the data from the file
    """
    reader = None
    _, suffix = os.path.splitext(fileName)

    if suffix.lower() in ('.h5', '.hdf5'):
        reader = GenericH5Reader()
    elif suffix.lower() in ('.jpg', '.png'):
        reader = ImageFileReader()
    elif suffix.lower() == '.mat':
        reader = MatlabReader()
    elif suffix.lower() == '.csv':
        reader = CSVReader()
    measurementData = reader.from_file(fileName)
    return measurementData


class ImageFileReader:
    def from_file(self, fileName):
        _, fileStr = os.path.split(fileName)
        try:
            imageData = imread(fileName)
        except OSError:
            return ImageMeasurementData('', None)
        return ImageMeasurementData(fileStr, imageData)


class GenericH5Reader:
    def from_file(self, fileName):
        dataCollection = {}

        def visitor_func(name, data):
            if isinstance(data, h5py.Dataset):
                dataCollection[name] = data[:]

        with h5py.File(fileName, 'r') as h5File:
            h5File.visititems(visitor_func)
        return NumericalMeasurementData(dataCollection)


class MatlabReader:
    def from_file(self, fileName):
        return NumericalMeasurementData(loadmat(fileName))


class CSVReader:
    def from_file(self, fileName):
        return NumericalMeasurementData({fileName: np.loadtxt(fileName)})
