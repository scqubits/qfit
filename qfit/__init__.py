# __init__.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import sys

from copy import deepcopy

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

import matplotlib

matplotlib.use("qtagg")

from qfit.core.mainwindow import MainWindow
from qfit.models.measurement_data import (
    dummy_measurement_data,
    MeasurementDataType,
)
from qfit.controllers.numerical_model import dummy_hilbert_space
from qfit.core.helpers import executed_in_ipython

from typing import Union

import scqubits as scq
from scqubits.core.hilbert_space import HilbertSpace

scq.settings.PROGRESSBAR_DISABLED = True



class qfit:
    window: MainWindow
    _hilbertSpace: HilbertSpace

    def __new__(
        cls, 
        hilbertSpace: HilbertSpace, 
        measurementData: MeasurementDataType
    ):
        # Create a new instance
        instance = object.__new__(cls)

        if not executed_in_ipython():
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            # QFontDatabase.addApplicationFont(":/fonts/Roboto-Regular.ttf")
            # font = QFontDatabase.font("Roboto", "", 10)
            # font.setWeight(QFont.Normal)
            # instance.app.setFont(font)
        else:
            # TODO
            pass

        instance._hilbertSpace = deepcopy(hilbertSpace)

        instance.window = MainWindow(
            measurementData = measurementData,
            hilbertspace = instance._hilbertSpace,
        )

        instance.window.show()

        return instance

    def __init__(self, hilbertSpace: HilbertSpace):
        self.window.ioMenuCtrl.newProject()

    @property
    def hilbertSpace(self) -> HilbertSpace:
        return self._hilbertSpace

    # @classmethod
    # def open(
    #     cls,
    #     hilbertSpace: HilbertSpace,
    #     measurementDataPath: Union[str, None] = None,
    # ):
        
    #     self = cls.__new__(cls, hilbertSpace, )


    #     self.window.ioMenuCtrl.openFile(measurementDataPath)


