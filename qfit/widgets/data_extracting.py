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


class DataExtractingWidget(QFrame):
    pass


class ListView(QListView):
    """
    A QListView: 
     - a custom signal: focusChanged. When user clicks on an item
     in the list, the row number of the clicked item is emitted.
     - a custom method: selectItem. Select (highlight) the item at the given index.
    """

    focusChanged = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionRectVisible(True)

    def setModel(self, model):
        """
        Set the model for the view and select the first item.
        """
        result = super().setModel(model)
        self.setCurrentIndex(model.index(0, 0))
        return result
    
    def currentChanged(self, current, previous):
        """
        When the current item changes, emit the focusChanged signal.
        """
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