from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QPushButton, QStackedWidget

from qfit.utils.helpers import modifyStyleSheet

from typing import TYPE_CHECKING, Tuple, Dict, Any


class PageView(QObject):
    """
    A view for the pages of the application. This view is responsible for
    switching between the different pages of the application.

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

    pageNames = ["setup", "calibrate", "extract", "prefit", "fit"]
    pageChanged = Signal(str)

    def __init__(
        self,
        parent: QObject,
        pageButtons: Dict[str, QPushButton],
        dataTransferButtons: Dict[str, QPushButton],
        stackWidgets: Dict[str, QStackedWidget],
    ):
        super().__init__(parent)
        self.pageButtons = pageButtons
        self.dataTransferButtons = dataTransferButtons
        self.stackWidgets = stackWidgets
        self.currentPage = list(pageButtons.keys())[0]

        self._staticInits()

    def _staticInits(self):
        """
        Initialize the view: connect the buttons to the corresponding slots.
        """
        for key, button in self.pageButtons.items():
            button.clicked.connect(lambda *args, key=key: self.switchToPage(key))

        # when clicked parameter export button, switch to the desired page
        for key, button in self.dataTransferButtons.items():
            if key not in self.pageNames:
                # contains "init" button
                continue
            button.clicked.connect(lambda *args, key=key: self.switchToPage(key))

    @Slot()
    def switchToPage(self, page: str):
        """
        Switch to the given page and emit the pageChanged signal.
        """
        if page == self.currentPage:
            return
        
        self.currentPage = page

        idx = self.pageNames.index(page)

        # switch the stack widget
        for widget in self.stackWidgets.values():
            widget.setCurrentIndex(idx)

        # set the corresponding button to checked
        for key, button in self.pageButtons.items():
            button.setChecked(key == page)

        self.pageChanged.emit(page)

    def setEnabled(self, enabled: bool, page: str | None = None):
        """
        Set whether the buttons are enabled or not. 

        Parameters
        ----------
        enabled : bool
            Whether the buttons are enabled or not.
        page : str | None
            The page to set the enabled state. If None, set all buttons.
        """
        if page is None:
            for button in self.pageButtons.values():
                button.setEnabled(enabled)
            for button in self.dataTransferButtons.values():
                button.setEnabled(enabled)
        else:
            self.pageButtons[page].setEnabled(enabled)
            if page in self.dataTransferButtons:
                self.dataTransferButtons[page].setEnabled(enabled)