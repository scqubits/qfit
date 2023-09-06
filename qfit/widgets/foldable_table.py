import numpy as np

from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
)
from PySide6.QtCore import (
    Qt,
)

from qfit.widgets.grouped_sliders import FoldPushButton
from qfit.core.helpers import modifyStyleSheet

from typing import List, Dict, Tuple, Union, Type

class CenteredItem(QWidget):
    """
    A container widget that centers its contents.
    """
    def __init__(self, widget):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)


class WidgetCollection:
    """
    A collection of widgets that represents a row in the table.
    """

    columns = []
    columnCount = 0

    def __init__(self, *args, **kwargs):
        self.widgetForInserting = {}

    def addWidget(self, key, widget):
        assert key in self.columns

        self.widgetForInserting[key] = CenteredItem(widget)


class FittingParameterItems(WidgetCollection):
    """
    A collection of widgets that represents a row in the FittingParameterTable.
    """

    columns = ["Name", "Fix", "Initial", "Min", "Max", "Current", ]
    columnCount = len(columns)

    def __init__(
        self,
        name: str,
    ):
        super().__init__()

        self.name = name

        self.nameLabel = QLabel(name)
        self.fixCheckbox = QCheckBox()
        self.initialValue = QLineEdit("")
        self.currentValue = QLabel("")
        self.minValue = QLineEdit("")
        self.maxValue = QLineEdit("")

        self.addWidget("Name", self.nameLabel)
        self.addWidget("Fix", self.fixCheckbox)
        self.addWidget("Initial", self.initialValue)
        self.addWidget("Current", self.currentValue)
        self.addWidget("Min", self.minValue)
        self.addWidget("Max", self.maxValue)

class MinMaxItems(WidgetCollection):
    """
    A collection of widgets that represents a row in the MinMaxTable. 
    (May not be a row actually)
    """

    columns = ["Name", "Min", "Max", ]
    columnCount = len(columns)

    def __init__(
        self,
        name: str,
    ):
        super().__init__()

        self.name = name

        self.nameLabel = QLabel(name)
        self.minValue = QLineEdit("")
        self.maxValue = QLineEdit("")

        self.addWidget("Name", self.nameLabel)
        self.addWidget("Min", self.minValue)
        self.addWidget("Max", self.maxValue)


class FoldableTable(QTableWidget):
    """
    A table widget whose rows can be folded and unfolded when a "group row"
    is clicked. Support browsing the contents using the group names.
    """

    def __init__(
        self,
        paramType: Type[WidgetCollection],
        paramNumPerRow: int,
        groupNames: List[str],
    ):
        super().__init__()

        self._paramType = paramType
        self._paramNumPerRow = paramNumPerRow
        
        # record the position of the groups
        self._groupNames: List[str] = groupNames
        self._groupRows: Dict[str, int] = dict(zip(
            self._groupNames, range(len(groupNames))
        ))

        # store the items in the table
        self._groupButtons: Dict[str, FoldPushButton] = {}
        self.params: Dict[str, Dict[str, WidgetCollection]] = {}

        # initialize the table with just the groups
        self.setColumnCount(paramNumPerRow * self._paramType.columnCount)
        self.setRowCount(0)
        self._initGroupRows()

        # configure the appearance of the table
        self._configure()

        # connect the buttons to the fold/unfold function
        for group in self._groupNames:
            # this might be an ugly way to do this
            # but `checked` and `group` are all required keywords 
            # arguments with default values. 
            
            # when the slot function with a single argument is called,
            # the argument is always the checked state of the button.

            # when the slot function with two arguments is called,
            # there will be no arguement to be passed...
            self._groupButtons[group].clicked.connect(
                lambda checked=False, group=group: self._onButtonClicked(group)
            )

        # set the default state of the group buttons
        self.setCheckable(True)
        self.setChecked(True)

    @property
    def _columns(self) -> List[str]:
        return self._paramType.columns * self._paramNumPerRow

    def _initGroupRows(self):
        """
        Initialize the groups.
        """
        for name in self._groupNames:
            self.insertRow(self.rowCount())
            self.setSpan(self.rowCount() - 1, 0, 1, self.columnCount())

            self._groupButtons[name] = FoldPushButton(name)
            self.params[name] = {}

            self.setCellWidget(self.rowCount() - 1, 0, self._groupButtons[name])

    def _insertParamRow(self, row_position):
        """
        Insert a row to the table after initialization. 
        """
        self.insertRow(row_position)

        # shift the group rows
        for name, value in self._groupRows.items():
            if value >= row_position:
                self._groupRows[name] += 1
                self._resizeTable()

    def _configure(self):
        """
        After initialization, configure the appearance of the table.
        """
        # Set the column widths.
        for idx, entry_type in enumerate(self._columns):
            width = 40 if entry_type in ["Name", "Fix"] else 60
            self.setHorizontalHeaderLabels(self._columns)
            self.setColumnWidth(idx, width)

        # disable the vertical header, grid, and frame
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setFrameShape(QTableWidget.NoFrame)

        # separate the group rows and the parameter rows by increasing 
        # the row height
        for row in self._groupRows.values():
            self.setRowHeight(row, 35)

        # set header and group names' style
        modifyStyleSheet(self.horizontalHeader(), "color", "white")
        for name in self._groupNames:
            modifyStyleSheet(self._groupButtons[name], "color", "white")

    def _resizeTable(self):
        # fix the height of the table
        self.setFixedHeight((
            self.horizontalHeader().height() 
            + np.sum([self.rowHeight(i) for i in range(self.rowCount())])
            + 2 * self.frameWidth()
            + self.horizontalScrollBar().height()
        ) * 1.2 + 10)   # need some offsets that I don't know why

        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()

    def setCheckable(self, value):
        """
        Set the checkable property of the group buttons.
        """
        for button in self._groupButtons.values():
            button.setCheckable(value)

    def setChecked(self, value):
        """
        Set the checked property of the group buttons.
        """
        for button in self._groupButtons.values():
            button.setChecked(value)

    def insertParams(self, group, name):
        """
        Insert a parameter row to the end of the table.
        """
        self.params[group][name] = self._paramType(name)

        # find the current section of the table
        group_row_idx = self._groupRows[group]

        # Since one parameter may occupy multiple columns, we need to
        # calculate the position of the parameter row / columns in the table.
        param_idx = len(self.params[group]) - 1      # which param
        param_row_idx = param_idx // self._paramNumPerRow
        param_column_idx = param_idx % self._paramNumPerRow

        current_row = param_row_idx + group_row_idx + 1  # +1 for the group row
        current_column = param_column_idx * self._paramType.columnCount

        # insert a row if it is the first parameter of a new row
        if param_column_idx == 0:
            self._insertParamRow(current_row)

        # insert the widgets
        for idx, entry_type in enumerate(self._paramType.columns):
            self.setCellWidget(
                current_row,
                current_column + idx,
                self.params[group][name].widgetForInserting[entry_type],
            )

    def _rowsBelow(self, group):
        """
        Return the rows below a group.
        """
        group_upper_row = self._groupRows[group] + 1
        try: 
            # it's the row of the next group
            group_lower_row = self._groupRows[self._groupNames[self._groupNames.index(group) + 1]]
        except IndexError:
            group_lower_row = self.rowCount()

        return range(group_upper_row, group_lower_row)

    def _fold(self, group):
        """
        Fold the content below a group by setting the rows to invisible.
        """
        for row in self._rowsBelow(group):
            self.setRowHidden(row, True)
    
    def _unfold(self, group):
        """
        Unfold the content below a group by setting the rows to visible.
        """

        for row in self._rowsBelow(group):
            self.setRowHidden(row, False)
        
    def _onButtonClicked(self, group):
        """
        Fold or unfold the content below a group.
        """
        if self._groupButtons[group].isChecked():
            self._unfold(group)
        else:
            self._fold(group)
