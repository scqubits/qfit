from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,

)        
from PySide6.QtWidgets import QPushButton, QStackedWidget

from typing import TYPE_CHECKING, Tuple, Dict, Any


class PageView(QObject):
    pageNames = ["calibrate", "extract", "prefit", "fit"]
    pageChanged = Signal(str)

    def __init__(
        self, 
        pageButtons: Dict[str, QPushButton],
        dataExportButtons: Dict[str, QPushButton],
        stackWidgets: Dict[str, QStackedWidget],
    ):
        super().__init__()
        self.pageButtons = pageButtons
        self.dataExportButtons = dataExportButtons
        self.stackWidgets = stackWidgets
        self.currentPage = "calibrate"

        self.staticInits()
        
    def staticInits(self):
        for key, button in self.pageButtons.items():
            button.clicked.connect(lambda *args, key=key: self._switchToPage(key))

        # when clicked parameter export button, switch to the desired page
        for key, button in self.dataExportButtons.items():
            button.clicked.connect(lambda *args, key=key: self._switchToPage(key))

    @Slot()
    def _switchToPage(self, page: str):
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