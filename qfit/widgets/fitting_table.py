from PySide6.QtWidgets import (
    QSlider,
    QLineEdit,
    QLabel,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QCheckBox,
    QTableWidget,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QCoreApplication

from qfit.widgets.grouped_sliders import FoldableWidget

import numpy as np
from typing import List, Dict, Tuple, Union

SPACING = 5

class FittingParameterRow(QWidget):
    """
    A collection of widgets that represents a row in the FittingParameterTable.
    """

    entry_types = ["Name", "Fix", "Initial", "Min", "Max", "Current", ]

    def __init__(
        self,
        name: str,
    ):
        self.name = name

        self.nameLabel = QLabel(name)
        self.fixCheckbox = QCheckBox()
        self.initialValue = QLineEdit("")
        self.currentValue = QLabel("")
        self.minValue = QLineEdit("")
        self.maxValue = QLineEdit("")

        self.widgetForInserting = {
            "Name": self.alignCenter(self.nameLabel),
            "Fix": self.alignCenter(self.fixCheckbox),
            "Initial": self.initialValue,
            "Current": self.alignCenter(self.currentValue),
            "Min": self.minValue,
            "Max": self.maxValue,
        }

    @staticmethod
    def alignCenter(widget) -> QWidget:
        container_widget = QWidget()
        layout = QHBoxLayout(container_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        return container_widget


class FittingParameterTable(QTableWidget):
    columns = FittingParameterRow.entry_types

    def __init__(
        self,
        row_names: List[str],
        parent=None,
    ):
        super().__init__(parent)

        # Set the table dimensions.
        self.setColumnCount(len(self.columns))
        self.setRowCount(0)

        # Set the column headers.
        self.setHorizontalHeaderLabels(self.columns)

        # insert the rows
        self.parameterWidgets: Dict[str, FittingParameterRow] = {}
        for name in row_names:
            self.insertParameter(name)

        # size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # configure the table layout
        self.configure()

    def configure(self):
        # Set the column widths.
        for idx, entry_type in enumerate(self.columns):
            width = 40 if entry_type in ["Name", "Fix"] else 60
            self.setColumnWidth(idx, width)

        # disable the vertical header, grid, and frame
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setFrameShape(QTableWidget.NoFrame)

        # set header style
        self.horizontalHeader().setStyleSheet("color: white")

        # fix the height of the table
        self.setFixedHeight(
            self.horizontalHeader().height() 
            + np.sum([self.verticalHeader().sectionSize(i) for i in range(self.rowCount())])
            + 2 * self.frameWidth()
            + self.horizontalScrollBar().height()
            + 10
        )

    def insertParameter(self, name):
        self.insertRow(self.rowCount())
        self.parameterWidgets[name] = FittingParameterRow(name)
        for idx, entry_type in enumerate(self.columns):
            self.setCellWidget(
                self.rowCount() - 1,
                idx,
                self.parameterWidgets[name].widgetForInserting[entry_type],
            )

    def keys(self):
        return self.parameterWidgets.keys()

    def values(self):
        return self.parameterWidgets.values()

    def items(self):
        return self.parameterWidgets.items()

    def __getitem__(self, key):
        return self.parameterWidgets[key]


class FittingParameterTableSet(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgetSetLayout = QVBoxLayout(self)
        self.widgetSetLayout.setContentsMargins(0, 0, 0, 0)  # Remove the margins
        self.widgetSetLayout.setSpacing(SPACING)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tables: Dict[str, FittingParameterTable] = {}

    def keys(self):
        return self.tables.keys()

    def values(self):
        return self.tables.values()

    def items(self):
        return self.tables.items()

    def __getitem__(self, key) -> FittingParameterTable:
        return self.tables[key]

    def addGroupedWidgets(
        self,
        set_name: str,
        row_names: List[str],
    ):
        # store the group
        self.tables[set_name] = FittingParameterTable(
            row_names=row_names,
            parent=self,
        )

        # add the group to the layout
        self.widgetSetLayout.addWidget(
            FoldableWidget(
                set_name,
                self.tables[set_name],
            )
        )
