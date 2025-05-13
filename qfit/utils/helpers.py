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
from labellines import labelLines

from PySide6 import QtCore as QtCore
from PySide6.QtWidgets import QWidget, QPushButton

from typing import Dict, List, Literal, Optional, Tuple, Union
from typing import TypeVar, Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.lines import Line2D
    from matplotlib.axes import Axes


Key = TypeVar("Key")
Value = TypeVar("Value")

try:
    # numpy < 2.0.0
    float_types = [float, *np.sctypes["float"]]
except AttributeError:
    # numpy > 2.0.0
    float_types = [float, np.float64, np.float32]


class DictItem(Generic[Key, Value]):
    """
    A class to represent a dictionary item with name and data.

    DictItem objects can be compared with each other using "==". However,
    the comparison is not recursive. It only compares the keys and values
    of the first level. For numpy arrays, it uses np.array_equal to compare
    the arrays so that it returns a single boolean value.

    Parameters
    ----------
    name: Key
        The name of the item.
    data: Value
        The data of the item.
    """

    def __init__(self, name: Key, data: Value):
        self.name: Key = name
        self.data: Value = data

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DictItem):
            return False

        if isinstance(self.data, np.ndarray | float) and isinstance(
            __value.data, np.ndarray | float
        ):
            if not np.array_equal(self.data, __value.data):
                return False
        else:
            if self.data != __value.data:
                return False

        return self.name == __value.name


class OrderedDictMod(OrderedDict[Key, Value], Generic[Key, Value]):
    """
    Mofiied OrderedDict with additional methods:

    Faster access to the keys and values of the dictionary:
        - valList: returns a list of the values
        - keyList: returns a list of the keys
        - itemByIndex: returns a DictItem by index
        - itemList: returns a list of DictItems

    Compare two dictionaries:
        - __eq__: compares two dictionaries. It only compares the keys
        and values of the first level, and does not compare nested
        dictionaries or numpy arrays.
    """

    @property
    def valList(self) -> List[Value]:
        return list(self.values())

    @property
    def keyList(self) -> List[Key]:
        return list(self.keys())

    def itemByIndex(self, itemIndex: int) -> DictItem[Key, Value]:
        """
        Returns a DictItem by index. DictItem is a class to represent
        a dictionary item with name and data.
        """
        return DictItem(self.keyList[itemIndex], self.valList[itemIndex])

    def itemList(self) -> List[DictItem[Key, Value]]:
        """
        Returns a list of DictItems. DictItem is a class to represent
        a dictionary item with name and data.
        """
        return [DictItem(key, val) for key, val in self.items()]

    def __eq__(self, __value: object) -> bool:
        """
        Compare two dictionaries. It only compares the keys and values
        of the first level. It does not compare nested dictionaries or
        numpy arrays.   -

        Parameters
        ----------
        dict1: dict
        dict2: dict

        Returns
        -------
        bool
        """
        if not isinstance(__value, OrderedDictMod):
            return False

        if self.keyList != __value.keyList:
            return False

        for key in self.keys():
            if type(self[key]) != type(__value[key]):
                return False

            if isinstance(self[key], np.ndarray | float) and isinstance(
                self[key], np.ndarray | float
            ):
                if not np.array_equal(self[key], __value[key]):
                    return False
            else:
                if self[key] != __value[key]:
                    return False
        return True


def isValid2dArray(array):
    """
    Checks whether the given array has the following properties:
        - Array entries must be real-valued
        - The array is strictly two-dimensional, i.e., number of rows>1
        and number of cols>1

    Parameters
    ----------
    array: ndarray

    Returns
    -------
    bool:
        True if all conditions above are satisfied.
    """
    if array.dtype not in float_types:
        return False
    if array.ndim == 2:
        if array.shape[0] > 1 and array.shape[1] > 1:
            return True
    return False


def isValid1dArray(array):
    """
    A valid 1d array must satisfy the following conditions:
        - Array entries must be real-valued
        - The array is strictly one-dimensional, i.e., number of rows=1 or number of cols=1
    """
    if array.dtype not in float_types:
        return False
    if array.ndim == 1:
        return True
        # return np.all(np.diff(array) > 0) or np.all(np.diff(array) < 0)
    if (array.ndim == 2) and (min(array.shape) == 1):
        return True
        # return np.all(np.diff(array.flatten()) > 0)
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


def makeUnique(names: List[str]):
    """
    Given a list of strings, return a list of unique strings by appending
    a number to the end of the string if the string is not unique.

    Example: ["a", "b", "a", "b", "a"] -> ["a", "b", "a (1)", "b (1)", "a (2)"]

    Parameters
    ----------
    names: List[str]
        A list of strings.

    Returns
    -------
    List[str]
        A list of unique strings in the same order as the input list.
    """
    unique_names = []
    for name in names:
        if name not in unique_names:
            unique_names.append(name)
        else:
            i = 1
            while f"{name} ({i})" in unique_names:
                i += 1
            unique_names.append(f"{name} ({i})")
    return unique_names


# widgets ######################################################################
def clearChildren(widget: QWidget):
    """
    Clear all children of the given widget.

    Parameters
    ----------
    widget: QWidget
    """
    layout = widget.layout()
    if layout is None:
        return
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget:  # Check if the item is a widget
            widget.setParent(None)
            widget.deleteLater()


def modifyStyleSheet(widget: QWidget, property_name: str, new_value: str):
    """
    Modify a particular stylesheet property of the given widget.

    Parameters
    ----------
    widget: QWidget
    property_name: str
        The name of the property to be modified.
    new_value: str
        The new value of the property.
    """
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


def disableButton(button: QPushButton, disable=True):
    """
    Disable or enable the given button.

    Parameters
    ----------
    button: QPushButton
    disable: bool
        Whether to disable the button or not.
    """
    button.setEnabled(not disable)

    if disable:
        modifyStyleSheet(button, "color", "gray")
    else:
        modifyStyleSheet(button, "color", "black")


# Plot #########################################################################
def filter(c, filter_name):
    """
    Apply a filter to the color.
    """
    if filter_name in ["translucent", "trans"]:
        r, g, b, a = c
        return [r, g, b, a * 0.2]
    elif filter_name in ["emphsize", "emph"]:
        r, g, b, a = c
        factor = 3
        return [r**factor, g**factor, b**factor, a]


class Cmap:
    """
    A wrapped class to represent a mpl colormap. It's kind of useless now,
    only used in the wrapped optimizer class, in a function that we don't
    use in QFit.

    Parameters
    ----------
    upper: float
        The upper limit of the colormap.
    lower: float
        The lower limit of the colormap.
    cmap_name: str
        The name of the colormap.
    """

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


# label lines ##################################################################
def _find_continuous_segments(
    xdata: np.ndarray,
    ydata: np.ndarray,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    min_segment_length: int = 2,
) -> List[List[int]]:
    """
    Find continuous segments of a line that are within axis limits and have no NaN values.

    Parameters
    ----------
    xdata, ydata : array-like
        The x and y data of the line
    xmin, xmax, ymin, ymax : float
        The axis limits
    min_segment_length : int, optional
        The minimum length of a segment to be considered valid

    Returns
    -------
    list of list of int
        List of segments, where each segment is a list of indices
    """
    segments = []
    current_segment = []

    for i, (x, y) in enumerate(zip(xdata, ydata)):
        if xmin <= x <= xmax and ymin <= y <= ymax and not np.isnan(y):
            current_segment.append(i)
        else:
            if len(current_segment) >= min_segment_length:
                segments.append(current_segment)
            current_segment = []

    # Don't forget the last segment
    if len(current_segment) >= min_segment_length:
        segments.append(current_segment)

    return segments


def _check_position_overlap(
    x_pos: float,
    y_pos: float,
    existing_lines: List["Line2D"],
    existing_positions: List[float],
    min_x_spacing: float,
    min_y_spacing: float,
) -> bool:
    """
    Check if a position overlaps with existing label positions.

    Parameters
    ----------
    x_pos, y_pos : float
        The position to check
    existing_lines : list of Line2D
        The existing lines with labels
    existing_positions : list of float
        The x-positions of existing labels
    min_x_spacing, min_y_spacing : float
        The minimum spacing between labels

    Returns
    -------
    bool
        True if the position is good (no overlap), False otherwise
    """
    for line, x in zip(existing_lines, existing_positions):
        # Get y-value at the existing label position
        existing_y = np.interp(x, line.get_xdata(), line.get_ydata())

        # Check both horizontal and vertical spacing
        if abs(x_pos - x) < min_x_spacing and abs(y_pos - existing_y) < min_y_spacing:
            return False

    return True


def _axPlotAndMimicLine(
    ax: "Axes",
    xdata: np.ndarray,
    ydata: np.ndarray,
    lineToMimic: "Line2D",
) -> "Line2D":
    """
    Mimic a line in the axes.
    """
    return ax.plot(
        xdata,
        ydata,
        color=lineToMimic.get_color(),
        linestyle=lineToMimic.get_linestyle(),
        linewidth=lineToMimic.get_linewidth(),
        alpha=lineToMimic.get_alpha(),
        zorder=lineToMimic.get_zorder(),
        label=lineToMimic.get_label(),
    )[0]


def labelLinesWithNans(
    ax: "Axes",
    lines: List["Line2D"],
    xlim: Tuple[float, float],
    ylim: Tuple[float, float],
    zorder: float = 2.0,
    alpha_factor: float = 1.0,
):
    """
    Find optimal locations for line labels that:
    - Are on visible parts of lines within axis limits
    - Avoid NaN values
    - Are placed on continuous segments with at least two points
    - Are spaced to avoid overlaps

    Then create invisible lines at the label positions and put a text label
    on them. Package `matplotlib-label-lines` can't label lines with nans
    properly, so we need to do this manually.

    Parameters
    ----------
    ax : Axes
        The axes to find label locations for
    lines : list of Line2D
        The lines to find label locations for
    xlim : Tuple[float, float]
        The x-axis limits
    ylim : Tuple[float, float]
        The y-axis limits

    Returns
    -------
    tuple
        (selected_lines, label_positions) - Lists of lines to label and their x-positions
    """
    xmin, xmax = xlim
    ymin, ymax = ylim

    # Calculate spacing parameters
    x_range = xmax - xmin
    y_range = ymax - ymin
    min_x_spacing = x_range * 0.1  # 10% of x-axis range
    min_y_spacing = y_range * 0.05  # 5% of y-axis range

    # Filter for visible lines with labels
    visible_lines = [
        line
        for line in lines
        if (
            line.get_visible() and line.get_label() and line.get_label() != "_nolegend_"
        )
    ]

    if not visible_lines:
        return [], []

    # store the selected lines and their label positions to label
    lines_to_label = []
    label_positions = []

    # Process each visible line
    for line in visible_lines:
        xdata: np.ndarray = line.get_xdata()  # type: ignore
        ydata: np.ndarray = line.get_ydata()  # type: ignore

        # Skip if line has no data points
        if len(xdata) == 0 or len(ydata) == 0:
            continue

        # Find continuous segments within axis limits
        segments = _find_continuous_segments(xdata, ydata, xmin, xmax, ymin, ymax)

        if not segments:
            continue  # No valid segments found

        # Sort segments by length (prefer longer segments)
        segments.sort(key=len, reverse=True)

        # Try to find a good position
        label_placed = False

        for segment in segments:
            # put labels at the middle of a subsegment of the segment (length = 2)
            # Try positions at 1/2, 2/5, 3/5, 1/5 and 4/5 of the segment
            segment_len = len(segment)
            if segment_len == 2:
                subsegments_to_try = [[segment[0], segment[1]]]
            else:
                idx_to_try = set(
                    [
                        int(segment_len * 1 / 2),
                        int(segment_len * 2 / 5),
                        int(segment_len * 3 / 5),
                        int(segment_len * 1 / 5),
                        int(segment_len * 4 / 5),
                    ]
                )
                # remove indices that are out of range
                idx_to_try = [
                    idx for idx in idx_to_try if 0 <= idx and idx + 1 < segment_len
                ]
                subsegments_to_try = [
                    [segment[idx], segment[idx + 1]] for idx in idx_to_try
                ]

            # Try each position
            for subseg_idx_0, subseg_idx_1 in subsegments_to_try:
                x_pos = (xdata[subseg_idx_0] + xdata[subseg_idx_1]) / 2
                y_pos = (ydata[subseg_idx_0] + ydata[subseg_idx_1]) / 2

                # Check if position is good (no overlap)
                if _check_position_overlap(
                    x_pos,
                    y_pos,
                    lines_to_label,
                    label_positions,
                    min_x_spacing,
                    min_y_spacing,
                ):
                    # create a new invisible line at the label position
                    # so that we can use the `labelLines` function to label it
                    new_line = _axPlotAndMimicLine(
                        ax, xdata[segment], ydata[segment], line
                    )
                    new_line.set_visible(False)

                    lines_to_label.append(new_line)
                    label_positions.append(x_pos)
                    label_placed = True
                    break

            if label_placed:
                break

        # If no good position found, use the middle of the longest segment
        if not label_placed and segments:
            longest_segment = segments[0]
            middle_idx = longest_segment[len(longest_segment) // 2]

            new_line = _axPlotAndMimicLine(
                ax, xdata[longest_segment], ydata[longest_segment], line
            )
            new_line.set_visible(False)

            lines_to_label.append(new_line)
            label_positions.append(xdata[middle_idx])

    if len(lines_to_label) > 0:
        labelLines(
            lines=lines_to_label,
            xvals=label_positions,
            zorder=zorder + 2.0,
            alpha=1.0 * alpha_factor,
        )


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

    return current_date_dir


# Function checking whether code is run from a jupyter notebook or inside ipython
def executed_in_ipython() -> bool:
    """
    Check if the code is executed in an IPython environment (e.g. Jupyter
    notebook or qtconsole of IPython).

    Returns
    -------
    bool
    """
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
def _closest_idx(arr, val):
    """
    find the index of the closest value in the array
    """
    return np.argmin(np.abs(arr - val))


def _find_lorentzian_peak(data: np.ndarray, gamma_guess=5.0) -> int:
    """
    fit the data with a Lorentzian function. The data is supposed to be taken from
    the two-tone spectroscopy, which is a 1D array of S21 values at selected freq
    range and a fixed voltage parameter.

    Parameters
    ----------
    data : np.ndarray
        The 1D data to be fitted.
    gamma_guess : float
        The initial guess of the gamma parameter (the width of the Lorentzian)
        in the unit of the index of the data.
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
        maxfev=300,
    )

    if np.sum(pcov) == np.inf:
        raise ValueError(
            "Lorentzian fit failed, potentially due to the data is "
            "flat in this region."
        )

    return np.round(popt[0]).astype(int)


def _extract_data_for_peak_finding(
    x_list: np.ndarray,
    y_list: np.ndarray,
    z_data: np.ndarray,
    user_selected_xy: Tuple[float, float],
    half_y_range: float = 0.1,
    min_points: int = 6,
):
    """
    Slice the 2D z_data and obtain a 1D array of z_data for fitting
    a Lorentzian peak. The length of the 1D array is determined by
    the half_y_range (minimal min_points in each direction).

    Parameters
    ----------
    x_list : np.ndarray
        The 1D x-axis data.
    y_list : np.ndarray
        The 1D y-axis data.
    z_data : np.ndarray
        The 2D z-axis data, containing the data to be sliced and fitted.
    user_selected_xy : Tuple[float, float]
        The x and y values of the point, near which the data will be sliced,
        and a Lorentzian peak will be found.
    half_y_range : float
        The half range of the y-axis data to be sliced.
    min_points : int
        The minimal number of points in each direction. It should be larger
        than 4, as we need at least 4 points to fit a Lorentzian peak.
    """
    x_val = user_selected_xy[0]
    y_val = user_selected_xy[1]
    y_min_val = y_val - half_y_range
    y_max_val = y_val + half_y_range
    # find the index of the selected point
    x_idx = _closest_idx(x_list, x_val)
    y_idx = _closest_idx(y_list, y_val)
    y_min_idx = _closest_idx(y_list, y_min_val)
    y_max_idx = _closest_idx(y_list, y_max_val)
    # translate to the min and max index of the y range; minimal number of points is
    # 6 for each direction. (Actually we just need 4 points to fit, but to make the
    # snapping functionality more visible, we use at least 12 pixels.)
    y_start = max(
        min(
            y_min_idx,
            y_max_idx,
            y_idx - min_points,
        ),
        0,
    )
    y_end = min(
        max(
            y_min_idx,
            y_max_idx,
            y_idx + min_points,
        ),
        len(y_list) - 1,
    )

    # extract data for fitting
    data_for_fitting = z_data[y_start : y_end + 1, x_idx]

    return y_start, y_end, data_for_fitting


def ySnap(
    x_list: np.ndarray,
    y_list: np.ndarray,
    z_data: np.ndarray,
    user_selected_xy: Tuple[float, float],
    half_y_range=0.1,
    mode="lorentzian",
) -> float:
    """
    Perform the y-snap for a selected point. A peak will be found in the
    vicinity of the selected point.

    Parameters
    ----------
    x_list : np.ndarray
        The 1D x-axis data.
    y_list : np.ndarray
        The 1D y-axis data.
    z_data : np.ndarray
        The 2D z-axis data, containing the data to be sliced and fitted.
    user_selected_xy : Tuple[float, float]
        The x and y values of the point, near which the data will be sliced,
        and a Lorentzian peak will be found.
    half_y_range : float
        The half range of the y-axis data to be sliced.
    mode : str
        The mode of the peak finding. It can be "lorentzian" or "extremum".
        For "lorentzian", the peak will be found by fitting a Lorentzian function
        to the data. For "extremum", the peak will be found by finding the maximum
        value of the data.

    Returns
    -------
    y: float
        The y value of the peak. If the peak finding fails, the y value of the
        selected point will be returned.
    """
    # translate range to left and right index
    y_min_idx, y_max_idx, data_for_peak_finding = _extract_data_for_peak_finding(
        x_list, y_list, z_data, user_selected_xy, half_y_range
    )

    # if the data is an image (has RGB channels), then make the data grayscale
    # by averaging the RGB channels
    if len(data_for_peak_finding.shape) == 2:
        data_for_peak_finding = data_for_peak_finding.mean(axis=1)

    # find the peaks
    if mode == "lorentzian":
        try:
            peak_idx = _find_lorentzian_peak(data_for_peak_finding)
        except Exception as e:
            return user_selected_xy[1]
    elif mode == "extremum":
        peak_idx = np.argmax(np.abs(data_for_peak_finding))

    return y_list[peak_idx + y_min_idx]
