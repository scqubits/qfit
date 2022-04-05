# manage_datasets.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from typing import TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget
from numpy import ndarray

import qfit.core.app_control as app_control
from qfit.ui_designer.ui_manage_datasets import Ui_ManageDatasetsWidget

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow


class ManageDatasetsWidget(QWidget):
    updateActiveDataset = Signal(ndarray)

    def __init__(self, parent: "MainWindow"):
        super(ManageDatasetsWidget, self).__init__(parent)
        self._model = None
        self.ui = Ui_ManageDatasetsWidget()
        self.ui.setupUi(self)

        for button in [
            self.ui.newRowButton,
            self.ui.deleteRowButton,
            self.ui.clearAllButton,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)


    @property
    def model(self):
        return self._model

    def setModel(self, model):
        self._model = model
        self.ui.datasetListView.setModel(model)
        self.set_connections()

    def set_connections(self):
        self.ui.newRowButton.clicked.connect(self.model.newRow)
        self.ui.newRowButton.clicked.connect(self.ui.datasetListView.setCurrentToLast)
        self.ui.deleteRowButton.clicked.connect(self.model.removeCurrentRow)
        self.ui.clearAllButton.clicked.connect(self.model.removeAll)

        self.ui.datasetListView.clicked.connect(
            lambda: self.updateActiveDataset.emit(self.model.currentAssocItem())
        )

        # A new selection of a data set item in ListView is accompanied by an update
        # of the canvas to show the appropriate plot of selected points
        self.ui.datasetListView.clicked.connect(
            lambda: app_control.CENTRAL.updatePlotSignal.emit(init=False)
        )

        # Each time the data set is changed on ListView/Model by clicking a data set,
        # the data in CurrentDatasetModel is updated to reflect the new selection.
        self.ui.datasetListView.clicked.connect(
            lambda: self.activeDataset.setAllData(
                newData=self.allDatasets.currentAssocItem()
            )
        )

        # A new selection of a data set item in ListView is accompanied by an update
        # of the canvas to show the appropriate plot of selected points
        self.ui.datasetListView.clicked.connect(
            lambda: app_control.CENTRAL.updatePlotSignal.emit(init=False)
        )

        # # Whenever tag type or tag data is changed, update the AllDatasetsModel data
        # self.tagDataView.changedTagType.connect(
        #     lambda: self.allDatasets.updateCurrentTag(self.tagDataView.getTag())
        # )
        # self.tagDataView.changedTagData.connect(
        #     lambda: self.allDatasets.updateCurrentTag(self.tagDataView.getTag())
        # )
        #
        # # Whenever a new dataset is activated in the AllDatasetsModel, update the TagDataView
        # self.ui.datasetListView.clicked.connect(
        #     lambda: self.tagDataView.setTag(self.allDatasets.currentTagItem())
        # )
