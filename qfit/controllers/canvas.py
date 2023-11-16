from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
)

from qfit.widgets.mpl_canvas import MplFigureCanvas




import sys
import os
import numpy as np
import copy

from typing import TYPE_CHECKING, Union, Dict, Any

if TYPE_CHECKING:
    from qfit.ui_designer.ui_window import Ui_MainWindow
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import (
        MeasurementDataType,
    )


class CursorCtrl:
    """
    Establishes the connection among the mpl canvas, the mpl toolbar, and the
    other user interfaces.
    """

    def __init__(
        self,
        mplCanvas: "MplFigureCanvas",
        ui: "Ui_MainWindow",
    ):
        pass
    
    # SpecialCursor's all_x_list update by allExtractedData change

    # Cursor's crosshair update by page switch & cursor mode button

    # Other MplFigureCanvas's controller related usage
