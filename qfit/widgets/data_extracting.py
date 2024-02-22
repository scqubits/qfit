# extractdata_view.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide6.QtCore import Slot, QItemSelectionModel, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QListView, QTableView

from qfit.utils.helpers import EditDelegate


class DataExtractingWidget(QFrame):
    pass


class DatasetWidget(QFrame):
    pass


class ManageDatasetsWidget(QFrame):
    pass


class TableView(QTableView):
    """Interface for the display of the table of extracted data points."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # style = "::section {""background-color: lightgray; }"
        # font = QFont()
        # font.setPointSize(9)
        # self.setFont(font)
        # self.horizontalHeader().setStyleSheet(style)
        # self.verticalHeader().setStyleSheet(style)
        self.setItemDelegate(EditDelegate())


class ListView(QListView):
    focusChanged = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # font = QFont()
        # font.setPointSize(9)
        # self.setFont(font)
        self.setSelectionRectVisible(True)

    def setModel(self, model):
        result = super().setModel(model)
        self.setCurrentIndex(model.index(0, 0))
        # self.setCurrentToLast()
        return result

    # def setCurrentToLast(self):
    #     """
    #     Set the current index to the last row of the list.
    #     """
    #     maxRowIndex = self.model().rowCount() - 1
    #     self.setCurrentIndex(self.model().index(maxRowIndex, 0))

    def currentChanged(self, current, previous):
        result = super().currentChanged(current, previous)
        self.focusChanged.emit(current.row())
        return result
    
    def selectItem(self, idx, blockSignals=False):
        """
        Select (highlight) the item at the given index.
        """
        if blockSignals:
            self.blockSignals(True)

        # set an item that has the keyboard focus
        self.setCurrentIndex(self.model().index(idx, 0))

        # select (highlight) an item visually
        self.selectionModel().select(
            self.model().index(idx, 0), QItemSelectionModel.ClearAndSelect
        )

        self.blockSignals(False)