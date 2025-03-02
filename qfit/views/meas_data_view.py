from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QPushButton, QTabWidget

from qfit.utils.helpers import modifyStyleSheet

from typing import TYPE_CHECKING, Tuple, Dict, Any, List


class MeasDataView(QObject):
    """
    A view for the measurement data. This view is responsible for
    switching between the different measurement data.

    Parameters
    ----------
    parent : QObject
        The parent object.
    pageButtons : Dict[str, QPushButton]
        The buttons that switch between the pages. The keys should be
        "calibrate", "extract", "prefit", "fit".
    dataTransferButtons : Dict[str, QPushButton]
        The buttons that transfer data between pages. The keys should be
        the destination page names: "prefit", "fit".
    stackWidgets : Dict[str, QStackedWidget]
        The stack widgets that contain the pages. The keys should be
        "calibrate", "extract", "prefit", "fit".
    """

    figChanged = Signal(str)
    figDeletedFromTab = Signal(int)

    def __init__(
        self,
        parent: QObject,
        dataTab: QTabWidget,
    ):
        super().__init__(parent)
        self.dataTab = dataTab

        self._staticInits()

    def _staticInits(self):
        """
        Initialize the view: connect the buttons to the corresponding slots.
        """
        # when clicked a different tab, emit a signal for switching the current page
        self.dataTab.currentChanged.connect(self.switchToFig)

    @Slot()
    def switchToFig(self, figIdx: int):
        """
        Switch to the given figure and emit the figChanged signal.
        """
        # if no figure is present (when all the figures are deleted), do nothing
        if figIdx == -1:
            return

        figName = self.dataTab.tabText(figIdx)

        self.figChanged.emit(figName)

    @Slot(list)
    def addFig(self, figNameList: List[str]):
        """
        Add a figure to the tab.
        """
        for figName in figNameList:
            self.dataTab.addTab(QPushButton(""), figName)
            # Set the tooltip for the newly added tab
            self.dataTab.setTabToolTip(self.dataTab.count() - 1, figName)
            # this changes the current index to the newly added tab
            # triggers currentChanged signal
        self.dataTab.setCurrentIndex(self.dataTab.count() - 1)

    @Slot(list)
    def reloadFig(self, figNameList: List[str]):
        """
        Reload the figures in the tab by providing a figure name list.
        """
        self.dataTab.clear()
        self.addFig(figNameList)

    @Slot()
    def deleteFig(self):
        """
        Remove the current figure from the tab.
        """
        removedFigIndex = self.dataTab.currentIndex()
        self.dataTab.removeTab(self.dataTab.currentIndex())

        # this changes the current index to the next tab
        # triggers currentChanged signal
        if self.dataTab.count() == 0:
            pass
        elif (
            removedFigIndex == self.dataTab.count()
        ):  # now row count is 1 less than before
            self.dataTab.setCurrentIndex(removedFigIndex - 1)
        else:
            self.dataTab.setCurrentIndex(removedFigIndex)

        self.figDeletedFromTab.emit(removedFigIndex)
