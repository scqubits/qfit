# mainwindow.py
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
from PySide6.QtCore import (
    QPoint,
    QRect,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle, QApplication
from PySide6.QtWidgets import QMainWindow
from qfit.models.registry import Registrable

from typing import Union, List


# metaclass: solve the incompatibility and make the mainWindow registrable
class CombinedMeta(type(QMainWindow), type(Registrable)):
    pass


class MainWindow(QMainWindow, Registrable, metaclass=CombinedMeta):
    """Class for the main window of the app."""

    closeWindow = Signal(object)
    _projectFile: Union[str, None]
    _unsavedChanges: bool
    attrToRegister: List[str] = ["_projectFile"]

    def __init__(self):
        QMainWindow.__init__(self)
        self._projectFile = None
        self._unsavedChanges = False        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setWindowIcon(QIcon(':/icons/svg/qfit-icon.svg'))

    def resizeAndCenter(self, maxSize: QSize):
        newSize = QSize(maxSize.width() * 0.9, maxSize.height() * 0.9)
        maxRect = QRect(QPoint(0, 0), maxSize)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, newSize, maxRect)
        )

    # Save Location & Window Title #####################################
    @property
    def projectFile(self):
        return self._projectFile

    @projectFile.setter
    def projectFile(self, value):
        self._projectFile = value
        self.setWindowTitleByProjectFile()

    @property
    def unsavedChanges(self):
        return self._unsavedChanges
    
    @unsavedChanges.setter
    def unsavedChanges(self, value):
        self._unsavedChanges = value
        self.setWindowTitleByProjectFile()

    def setWindowTitleByProjectFile(self):
        if self.projectFile is not None:
            windowTitle = f"qfit - {os.path.basename(self.projectFile)}"
        else:
            windowTitle = "qfit"

        # it is useless now (as it will only be updated when user clicks "save" / "close"...)
        # if self.unsavedChanges:
        #     windowTitle += " *"

        self.setWindowTitle(windowTitle)

    # register #########################################################
    def registerAll(self):
        """
        After registering the models,
        Register the rest attribute of the mainWindow.
        """
        registryDict = {}
        for attr in self.attrToRegister:
            entry = self._toRegistryEntry(attr)
            registryDict[entry.name] = entry

        return registryDict
    
    # signals ##########################################################
    def closeEvent(self, event):
        """
        Override the original class method to add a confirmation dialog before
        closing the application. Will be triggered when the user clicks the "X"
        or call the close() method.
        """
        super().closeEvent(event)
        self.closeWindow.emit(event)
