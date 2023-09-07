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
import os

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
from qfit.io_utils.measurement_file_readers import readMeasurementFile
from qfit.controllers.io_menu import IOCtrl

from typing import Union

import scqubits as scq
from scqubits.core.hilbert_space import HilbertSpace

scq.settings.PROGRESSBAR_DISABLED = True


class qfit:
    app: Union[QApplication, None] = None
    window: MainWindow
    _hilbertSpace: HilbertSpace

    @classmethod
    def _newProject(
        cls, 
        hilbertSpace: HilbertSpace, 
        measurementData: Union[MeasurementDataType, None] = None
    ) -> "qfit":
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
            instance.app = app
        else:
            # TODO
            pass

        instance._hilbertSpace = deepcopy(hilbertSpace)
        if measurementData is None:
            measurementData = dummy_measurement_data()

        instance.window = MainWindow(
            measurementData = measurementData,
            hilbertspace = instance._hilbertSpace,
        )

        instance.window.show()

        return instance
    
    def __new__(
        cls,
        hilbertSpace: HilbertSpace, 
        measurementData: Union[str, None] = None
    ) -> "qfit":
        instance = cls._newProject(
            hilbertSpace, None) 

        return instance           

    def __init__(
        self, 
        hilbertSpace: HilbertSpace, 
        measurementFileName: Union[str, None] = None
    ):
        # check if file exists
        if measurementFileName is not None:
            if not os.path.isfile(measurementFileName):   
                raise FileNotFoundError(f"File '{measurementFileName}' does not exist.")
            
        if measurementFileName is not None:
            # load measurement data from the given file
            measurementData = IOCtrl.measurementDataFromFile(measurementFileName)
            if measurementData is None:
                raise FileNotFoundError(f"Can't load file '{measurementFileName}'.")
            self.window.ioMenuCtrl.newProjectWithMeasurementData(measurementData)
        else:
            # open a window to ask for a file
            self.window.ioMenuCtrl.newProject(from_menu=False)

        if not executed_in_ipython():
            self.app.exec_()

    @property
    def hilbertSpace(self) -> HilbertSpace:
        return self._hilbertSpace

    # methods to create a new project #########################################
    @classmethod
    def new(
        cls,
        hilbertSpace: HilbertSpace,
        measurementFileName: Union[str, None] = None,
    ) -> "qfit":
        """
        Create a qfit project with a `HilbertSpace object` from `scqubits` and
        a measurement file.

        Parameters
        ----------
        hilbertSpace: HilbertSpace
            HilbertSpace object from scqubits
        measurementFileName: str
            Name of measurement file to be loaded. If left blank, a window
            will pop up to ask for a file.

        Returns
        -------
        qfit project
        """

        # check if file exists
        if measurementFileName is not None:
            if not os.path.isfile(measurementFileName):   
                raise FileNotFoundError(f"File '{measurementFileName}' does not exist.")
            
        instance = cls._newProject(
            hilbertSpace, dummy_measurement_data())
        
        # load measurement data
        if measurementFileName is not None:
            measurementData = IOCtrl.measurementDataFromFile(measurementFileName)
            if measurementData is None:
                raise FileNotFoundError(f"Can't load file '{measurementFileName}'.")
            instance.window.ioMenuCtrl.newProjectWithMeasurementData(measurementData)
        else:
            instance.window.ioMenuCtrl.newProject(from_menu=False)

        if not executed_in_ipython():
            instance.app.exec_()

        return instance

    @classmethod
    def open(
        cls, 
        fileName: Union[str, None] | None = None,
    ) -> "qfit":
        """
        Open a qfit project from a file.

        Parameters
        ----------
        fileName: str
            Name of file to be opened.

        Returns
        -------
        qfit project
        """

        # check if file exists
        if fileName is not None:
            if not os.path.isfile(fileName):
                raise FileNotFoundError(f"File '{fileName}' does not exist.")

        instance = cls._newProject(
            dummy_hilbert_space(), dummy_measurement_data())
        
        # load registry
        if fileName is None:
            fileName = instance.window.ioMenuCtrl.openFile(from_menu=False)
        else:
            registryDict = IOCtrl.registryDictFromFile(fileName)
            if registryDict is None:
                raise FileNotFoundError(f"Can't load file '{fileName}'.")
            
            instance.window.ioMenuCtrl.openProjectWithRegistryDict(registryDict)

        if not executed_in_ipython():
            instance.app.exec_()

        return instance
