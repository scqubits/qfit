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


from PySide6.QtCore import Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QListView, QTableView

from qfit.core.helpers import EditDelegate


class TableView(QTableView):
    """Interface for the display of the table of extracted data points."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setItemDelegate(EditDelegate())


class ListView(QListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionRectVisible(True)

    def setModel(self, model):
        result = super().setModel(model)
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