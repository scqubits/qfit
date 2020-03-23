# misc.py
#
# This file is part of datapyc.
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
from PySide2.QtWidgets import QStyledItemDelegate, QLineEdit


class EditDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

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
