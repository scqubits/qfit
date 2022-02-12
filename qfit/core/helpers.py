# helpers.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from collections import OrderedDict

import numpy as np

from PySide2 import QtCore as QtCore
from PySide2.QtCore import QLocale
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QLineEdit, QStyledItemDelegate


class EditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = DoubleLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, role=QtCore.Qt.DisplayRole))


class DoubleLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(DoubleValidator())

    def value(self):
        return float(self.text())


class DoubleValidator(QDoubleValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        localeSetting = QLocale()
        localeSetting.setNumberOptions(QLocale.RejectGroupSeparator)
        self.setLocale(localeSetting)


class OrderedDictMod(OrderedDict):
    @property
    def valList(self):
        return list(self.values())

    @property
    def keyList(self):
        return list(self.keys())

    def itemByIndex(self, itemIndex):
        return DataItem(self.keyList[itemIndex], self.valList[itemIndex])

    def itemList(self):
        return [DataItem(key, val) for key, val in self.items()]


class DataItem:
    def __init__(self, name, data):
        self.name = name
        self.data = data


def isValid2dArray(array):
    """
    Checks whether the given array has the following properties:
    * Array entries must be real-valued
    * The array is strictly two-dimensional, i.e., number of rows>1 and number of cols>1
    * The array does not merely repeat a single row or a single column n times

    Parameters
    ----------
    array: ndarray

    Returns
    -------
    bool:
        True if all conditions above are satisfied.
    """
    if array.dtype not in [float, np.float_, np.float64, np.float32]:
        return False
    if array.ndim == 2:
        if array.shape[0] > 1 and array.shape[1] > 1:
            if (array[0] != array[1]).any() or (array[:, 0] != array[:, 1]).any():
                return True
    return False


def isValid1dArray(array):
    if array.dtype not in [float, np.float_, np.float64, np.float32]:
        return False
    if array.ndim == 1:
        return np.all(np.diff(array) > 0)
    if (array.ndim == 2) and (min(array.shape) == 1):
        return np.all(np.diff(array.flatten()) > 0)
    return False


def hasIdenticalRows(array):
    return (array == array[0]).all()


def hasIdenticalCols(array):
    return (array.transpose == array.transpose()[0]).all()


def transposeEach(xyDataList):
    """
    Helper function that transposes each data set in the list. Used when importing DatapycData and converting back
    to data format used in AllExtractedDataModel

    Parameters
    ----------
    xyDataList: list of ndarray
        Each ndarray is of the form array([[x1,y1], [x2,y2], ...]).

    Returns
    -------
    list of ndarray
        Each ndarray has the form array([[x1, x2, ...], [y1, y2, ...]])
    """
    return [array.transpose() for array in xyDataList]


def remove_nones(dict_data):
    return {key: value for key, value in dict_data.items() if value is not None}
