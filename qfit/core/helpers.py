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

import os, time
import re
from collections import OrderedDict

import numpy as np

# import pandas as pd

from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
from matplotlib import colormaps

from PySide6 import QtCore as QtCore
from PySide6.QtCore import QLocale
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QLineEdit, QStyledItemDelegate, QWidget

from typing import Dict, List, Literal, Optional, Tuple, Union


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
    """
    A valid 1d array must satisfy the following conditions:
    * Array entries must be real-valued
    * The array is strictly one-dimensional, i.e., number of rows=1 or number of cols=1
    * The array increases monotonically
    """
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
    Helper function that transposes each data set in the list. Used when importing QfitData and converting back
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


# widgets ######################################################################
def clearChildren(widget: QWidget):
    layout = widget.layout()
    if layout is None:
        return
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget:  # Check if the item is a widget
            widget.setParent(None)
            widget.deleteLater()

def modifyStyleSheet(widget, property_name, new_value):
    # Get the current stylesheet
    current_style = widget.styleSheet()

    # Use regex to find and replace the property value
    pattern = re.compile(f"{property_name}:\\s*[^;]+;")
    replacement = f"{property_name}: {new_value};"

    # check if the property exists
    if pattern.search(current_style) is None:
        # add the property
        modified_style = current_style + replacement
    else:
        modified_style = re.sub(pattern, replacement, current_style)

    # Set the modified stylesheet back to the widget
    widget.setStyleSheet(modified_style)


# Plot #########################################################################
def filter(c, filter_name):
    if filter_name in ["translucent", "trans"]:
        r, g, b, a = c
        return [r, g, b, a * 0.2]
    elif filter_name in ["emphsize", "emph"]:
        r, g, b, a = c
        factor = 3
        return [r**factor, g**factor, b**factor, a]


class Cmap:
    def __init__(self, upper: float, lower: float = 0, cmap_name="rainbow"):
        self.upper = upper
        self.lower = lower
        self.cmap_name = cmap_name

        self.cmap = colormaps[self.cmap_name]
        self.norm = plt.Normalize(self.lower, self.upper)
        self.mappable = plt.cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def __call__(self, val):
        # return self.mappable.cmap(val)
        return self.cmap(self.norm(val))


# Save csv ######################################################################


def datetime_dir(
    save_dir="./",
    dir_suffix=None,
):
    """
    Initialize a directory with the current datetime.

    Parameters & Examples
    ---------------------
    save_dir : str
        The directory to save the data, default to be "./". Say the current
        datetime is 2021-01-31 12:34, then the directory will be
        "save_dir/Jan/31_12-34/".
    dir_suffix : str
        The suffix of the directory, default to be None. Say the current
        datetime is 2021-01-31 12:34, then the directory will be
        "save_dir/Jan/31_12-34_dir_suffix/".

    Returns
    -------
    current_date_dir : str
    """
    save_dir = os.path.normpath(save_dir)

    current_time = time.localtime()
    current_month_dir = save_dir + time.strftime("/%h/", current_time)
    current_date_dir = current_month_dir + time.strftime("%d_%H-%M", current_time)

    if dir_suffix != "" and dir_suffix is not None:
        current_date_dir = current_date_dir + "_" + dir_suffix + "/"
    else:
        current_date_dir = current_date_dir + "/"

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if not os.path.exists(current_month_dir):
        os.mkdir(current_month_dir)
    if not os.path.exists(current_date_dir):
        os.mkdir(current_date_dir)

    # print(f"Current datetime directory: {current_date_dir}")
    return current_date_dir


# Function checking whether code is run from a jupyter notebook or inside ipython
def executed_in_ipython():
    try:  # inside ipython, the function get_ipython is always in globals()
        shell = get_ipython().__class__.__name__
        if shell in ["ZMQInteractiveShell", "TerminalInteractiveShell"]:
            return True  # Jupyter notebook or qtconsole of IPython
        return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


class StopExecution(Exception):
    def _render_traceback_(self):
        pass


# peak finding #################################################################
def _find_lorentzian_peak(data: np.ndarray, gamma_guess=5) -> int:
    """
    fit the data with a Lorentzian function. The data is supposed to be taken from
    the two-tone spectroscopy, which is a 1D array of S21 values at selected freq
    range and a fixed voltage parameter.
    """
    freq_list_length = len(data)
    idx_list = np.arange(freq_list_length)

    # fit the data with a 1D Lorentzian function
    lorentzian = (
        lambda idx, mid_idx, gamma, amp, bias: amp
        * (gamma / 2)
        / ((idx - mid_idx) ** 2 + (gamma / 2) ** 2)
        + bias
    )

    # guess
    gamma_guess = gamma_guess
    bias_guess = np.mean(data)
    mid_idx_guess = np.argmax(np.abs(data - bias_guess))
    amp_guess = data[mid_idx_guess] - bias_guess

    popt, pcov = curve_fit(
        lorentzian,
        idx_list,
        data,
        p0=[mid_idx_guess, gamma_guess, amp_guess, bias_guess],
        maxfev=2000,
    )

    return np.round(popt[0]).astype(int)


def _extract_data_for_peak_finding(
    x_list, y_list, z_data, user_selected_xy, half_index_range: int = 5
):
    """
    extract data for peak finding
    """
    frequency_point_count = len(y_list)
    x_val = user_selected_xy[0]
    y_val = user_selected_xy[1]
    # find the index of the selected point
    x_idx = np.argmin(np.abs(x_list - x_val))
    y_idx = np.argmin(np.abs(y_list - y_val))
    # translate to the min and max index of the y range
    y_min_idx = np.max([y_idx - half_index_range, 0])
    y_max_idx = np.min([y_idx + half_index_range, frequency_point_count - 1])

    # extract data for fitting
    data_for_fitting = z_data[y_min_idx : y_max_idx + 1, x_idx]

    return y_min_idx, y_max_idx, data_for_fitting


def y_snap(
    x_list, y_list, z_data, user_selected_xy, half_index_range=5, mode="lorentzian"
) -> Tuple[int, int]:
    """
    perform the y-snap for a selected point, such that the nearest peak in
    the vicinity will be selected instead.

    Parameters
    ----------
    y_list : List
        the y_list of the data
    data : List
        the data
    peak_tuple : Tuple
        the peak (x, y) indexes that will be polished
    index_range : int
        a new peak will be found within the range of the index

    Returns
    -------
        (x, y), new peak
    """
    # translate range to left and right index
    y_min_idx, y_max_idx, data_for_peak_finding = _extract_data_for_peak_finding(
        x_list, y_list, z_data, user_selected_xy, half_index_range
    )

    # find the peaks
    if mode == "lorentzian":
        peak_idx = _find_lorentzian_peak(data_for_peak_finding)
    elif mode == "extremum":
        peak_idx = np.argmax(np.abs(data_for_peak_finding))

    return y_list[peak_idx + y_min_idx]


# def save_variable_dict(file_name, variable_dict: Dict[str, float]):
#     """
#     Save a dictionary contains name-value pairs to a csv file.
#     """
#     new_dict = dict([(key, [val]) for key, val in variable_dict.items()])
#     pd.DataFrame.from_dict(
#         new_dict,
#         orient="columns",
#     ).to_csv(file_name)

# def load_variable_dict(file_name) -> Dict[str, float]:
#     """
#     Load a dictionary contains name-value pairs from a csv file. The file should be
#     saved by save_variable_dict.
#     """
#     list_dict = pd.read_csv(
#         file_name,
#         index_col=0,
#         header=0
#     ).to_dict(orient='list')
#     new_dict = dict([(key, val[0]) for key, val in list_dict.items()])
#     return new_dict

# def save_variable_list_dict(
#     file_name,
#     variable_list_dict: Dict[str, np.ndarray],
#     orient: Literal['columns', 'index'] = 'columns',
# ) -> None:
#     """
#     Save a dictionary contains name-value_list pairs to a csv file.

#     orient = 'index' SHOULD be used when variable list are not equal in length
#     """
#     pd.DataFrame.from_dict(
#         variable_list_dict,
#         orient=orient,
#     ).to_csv(file_name)

# def load_variable_list_dict(
#     file_name,
#     throw_nan = True,
#     orient: Literal['columns', 'index'] = 'columns'
# ) -> Dict[str, np.ndarray]:
#     """
#     Load a dictionary contains name-value_list pairs from a csv file. The file should be
#     saved by save_variable_list_dict.

#     throw_nan : bool
#         If True, remove nan in the list. It's useful when the list is not equal in length.

#     orient = 'index' should be used when variable list are not equal in length
#     """
#     if orient == 'index':
#         variable_list_dict = pd.read_csv(
#             file_name, index_col=0, header=0).transpose().to_dict(orient='list')
#     elif orient == 'columns':
#         variable_list_dict = pd.read_csv(
#             file_name, index_col=0, header=0).to_dict(orient='list')
#     else:
#         raise ValueError("only recognize 'index' or 'columns' for orient")

#     if not throw_nan:
#         return dict([(key, np.array(val)) for key, val in variable_list_dict.items()])

#     for key, val in variable_list_dict.items():
#         new_val = np.array(val)
#         new_val = new_val[~np.isnan(val)]
#         variable_list_dict[key] = new_val
#     return variable_list_dict
