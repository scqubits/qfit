# extractdata_view.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide2.QtCore import Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QListView, QTableView

from datapyc.core.helpers import EditDelegate


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # font = QFont()
        # font.setPointSize(9)
        # self.setFont(font)
        self.setSelectionRectVisible(True)

    def setModel(self, model):
        result = super().setModel(model)
        # self.model().rowsRemoved.connect(self.setCurrentToLast)
        # self.model().rowsInserted.connect(self.setCurrentToLast)
        self.setCurrentToLast()
        return result

    @Slot()
    def setCurrentToLast(self):
        maxRowIndex = self.model().rowCount() - 1
        self.setCurrentIndex(self.model().index(maxRowIndex, 0))

    def currentChanged(self, current, previous):
        result = super().currentChanged(current, previous)
        self.model().setCurrentRow(current)
        return result
