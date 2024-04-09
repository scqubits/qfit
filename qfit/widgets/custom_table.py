import numpy as np

from PySide6.QtWidgets import (
    QWidget,
    QTableWidget,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QTableWidgetItem,
    QSizePolicy,
    QSpacerItem,
    QHeaderView,
    QStyleOptionHeader,
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import (
    QColor,
    QTextDocument,
    QAbstractTextDocumentLayout,
    QTextOption,
)

from qfit.widgets.foldable_widget import FoldPushButton
from qfit.utils.helpers import modifyStyleSheet
from qfit.widgets.validated_line_edits import FloatLineEdit

from typing import List, Dict, Tuple, Union, Type, Generic, TypeVar


class CenteredItem(QWidget):
    """
    A container widget that centers its contents.
    """

    def __init__(self, parent, widget):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addItem(QSpacerItem(5, 0, QSizePolicy.Fixed))
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        layout.addItem(QSpacerItem(5, 0, QSizePolicy.Fixed))
        # inherit the style sheet from the widget
        self.setStyleSheet(widget.styleSheet())


class NoSeparatorHeaderView(QHeaderView):
    """
    A header view that does not draw the separator between columns.

    Parameters
    ----------
    orientation : Qt.Orientation
        The orientation of the header view.
    parent : QWidget
        The parent widget. By default None.
    color_list : List[str], optional
        A list of color strings for each header item, by default None.
    text_color : str, optional
        The color of the text, can be specified in various formats, by default
        "#ffffff", the white color in hex format.
    """

    def __init__(
        self,
        orientation,
        parent=None,
        color_list: List[str] = None,
        text_color: str = "#ffffff",
    ):
        super(NoSeparatorHeaderView, self).__init__(orientation, parent)
        self.colorList = color_list
        self.text_color = text_color
        # change the header color and style
        modifyStyleSheet(self, "font", '13px "Roboto Medium"')
        modifyStyleSheet(self, "font-weight", "bold")

    def paintSection(self, painter, rect, logicalIndex):
        """
        Paint the section of the header.

        Parameters
        ----------
        painter : QPainter
            The painter object.
        rect : QRect
            The rectangle of the section.
        logicalIndex : int
            The logical index of the section.
        """
        painter.save()

        # Set up the painter
        # loop over the color list for each header item
        # if None in the color list, make it transparent
        if self.colorList is not None:
            if self.colorList[logicalIndex] is not None:
                painter.fillRect(rect, QColor(self.colorList[logicalIndex]))
            else:
                painter.fillRect(rect, QColor(Qt.transparent))

        # Initialize QTextDocument for rich text (HTML) support
        textDocument = QTextDocument()
        textDocument.setDefaultFont(painter.font())

        # Disable word wrapping
        textOption = QTextOption()
        textOption.setAlignment(Qt.AlignCenter)  # Center alignment
        textOption.setWrapMode(QTextOption.NoWrap)  # Disable word wrapping
        textDocument.setDefaultTextOption(textOption)

        # Use HTML to set text color and wrap content in a div with center alignment
        headerText = self.model().headerData(
            logicalIndex, self.orientation(), Qt.DisplayRole
        )
        textDocument.setHtml(
            f'<div style="color: {self.text_color};">{headerText}</div>'
        )
        textDocument.setTextWidth(rect.width())  # Ensure adequate width

        # Calculate yOffset for vertical centering
        textHeight = textDocument.size().height()
        yOffset = (rect.height() - textHeight) / 2

        painter.translate(rect.left(), rect.top() + yOffset)

        # Draw the document contents
        textDocument.documentLayout().draw(
            painter, QAbstractTextDocumentLayout.PaintContext()
        )

        painter.restore()


class WidgetCollection:
    """
    A collection of widgets that represents a row in the table.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    """

    columns = []
    columnBackgroundColors = {}
    columnCount = 0

    def __init__(self, parent, name):
        self.widgetForInserting = {}
        self.parent = parent
        self.name = name

    def addWidget(self, key, widget):
        """
        Add a widget to the collection.

        Parameters
        ----------
        key : str
            The name of the column.
        widget : QWidget
            The widget to be added.
        """
        assert key in self.columns

        self.widgetForInserting[key] = CenteredItem(self.parent, widget)


class FittingParameterItems(WidgetCollection):
    """
    A collection of widgets that represents a row in the FittingParameterTable.
    It contains the widgets for each fitting parameter, namely the name, the
    fix checkbox, the initial value, the minimum value, the maximum value, and
    the result value.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    name : str
        The name of the parameter.
    """

    columns = [
        "NAME",
        "FIX",
        "INITIAL",
        "MIN",
        "MAX",
        "RESULT",
    ]
    # the background color of each column
    # None = default (transparent)
    # based on the UI/UX design
    columnBackgroundColors = {
        "NAME": None,
        "FIX": None,
        "INITIAL": "#292929",
        "MIN": None,
        "MAX": "#292929",
        "RESULT": "#363636",
    }
    # column widths
    columnWidths = {
        "NAME": 115,
        "FIX": 30,
        "INITIAL": 70,
        "MIN": 70,
        "MAX": 70,
        "RESULT": 70,
    }
    columnCount = len(columns)

    def __init__(
        self,
        parent,
        name: str,
    ):
        super().__init__(parent, name)

        self.nameLabel = QLabel(name)
        self.fixCheckbox = QCheckBox()
        self.initialValue = FloatLineEdit("")
        self.resultValue = QLabel("")
        self.minValue = FloatLineEdit("")
        self.maxValue = FloatLineEdit("")
        # keep them in a dict
        self.entriesDict = {
            "NAME": self.nameLabel,
            "FIX": self.fixCheckbox,
            "INITIAL": self.initialValue,
            "RESULT": self.resultValue,
            "MIN": self.minValue,
            "MAX": self.maxValue,
        }
        # loop over the dict to set the style sheet
        for key, value in self.entriesDict.items():
            modifyStyleSheet(value, "color", "white")
            # change the border color of the line edit
            if isinstance(value, FloatLineEdit):
                modifyStyleSheet(value, "border", "1px solid #5F5F5F")
            value.setMinimumSize(45, 20)
            if self.columnBackgroundColors[key] is not None:
                modifyStyleSheet(
                    value, "background-color", self.columnBackgroundColors[key]
                )
            self.addWidget(key, value)


class MinMaxItems(WidgetCollection):
    """
    A collection of widgets that represents a row in the MinMaxTable.
    It contains the widgets for each slider parameter, namely the name, the
    minimum value, and the maximum value.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    name : str
        The name of the parameter.
    """

    columns = [
        "NAME",
        "MIN",
        "MAX",
    ]
    # the background color of each column
    # None = default (transparent)
    columnBackgroundColors = {
        "NAME": "#212121",
        "MIN": "#292929",
        "MAX": "#363636",
    }
    # column widths
    columnWidths = {
        "NAME": 115,
        "MIN": 130,
        "MAX": 130,
    }
    columnCount = len(columns)

    def __init__(
        self,
        parent,
        name: str,
    ):
        super().__init__(parent, name)

        self.nameLabel = QLabel(name)
        self.minValue = FloatLineEdit("")
        self.maxValue = FloatLineEdit("")
        # keep them in a dict
        self.entriesDict = {
            "NAME": self.nameLabel,
            "MIN": self.minValue,
            "MAX": self.maxValue,
        }

        self.addWidget("NAME", self.nameLabel)
        self.addWidget("MIN", self.minValue)
        self.addWidget("MAX", self.maxValue)
        # loop over the dict to set the style sheet
        for key, value in self.entriesDict.items():
            modifyStyleSheet(value, "color", "white")
            value.setMinimumSize(45, 20)
            # change the border color of the line edit
            if isinstance(value, FloatLineEdit):
                modifyStyleSheet(value, "border", "1px solid #5F5F5F")
            if self.columnBackgroundColors[key] is not None:
                modifyStyleSheet(
                    value, "background-color", self.columnBackgroundColors[key]
                )
            self.addWidget(key, value)


CollectionType = TypeVar("CollectionType", bound=WidgetCollection)


class FoldableTable(QTableWidget, Generic[CollectionType]):
    """
    A table widget whose rows can be folded and unfolded when a "group row"
    is clicked. Support browsing the contents using the group names.

    Parameters
    ----------
    paramType : Type[CollectionType]
        The type of the parameter collection, which stores the widgets for each
        parameter. It should be a subclass of WidgetCollection.
    paramNumPerRow : int
        The number of parameters per row.
    groupNames : List[str]
        The names of the groups, and contents in the same group can be
        folded and unfolded together.
    """

    def __init__(
        self,
        paramType: Type[CollectionType],
        paramNumPerRow: int,
        groupNames: List[str],
    ):
        super().__init__()

        self._paramType = paramType
        self._paramNumPerRow = paramNumPerRow

        # replace the default header view with a custom one
        header = NoSeparatorHeaderView(
            Qt.Horizontal,
            color_list=list(self._paramType.columnBackgroundColors.values()),
            text_color="#AAAAAA",
        )
        header.setModel(self.model())  # Make sure to set the model for the header
        self.setHorizontalHeader(header)

        # record the position of the groups
        self._groupNames: List[str] = groupNames
        self._groupRows: Dict[str, int] = dict(
            zip(self._groupNames, range(len(groupNames)))
        )

        # store the items in the table
        self._groupButtons: Dict[str, FoldPushButton] = {}
        self.params: Dict[str, Dict[str, CollectionType]] = {}

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
        # TODO why the table has to be checkable?
        self.setCheckable(True)
        self.setChecked(True)

    def keys(self):
        return self.params.keys()

    def values(self):
        return self.params.values()

    def items(self):
        return self.params.items()

    def __getitem__(self, key: str) -> Dict[str, CollectionType]:
        return self.params[key]

    @property
    def _columns(self) -> List[str]:
        return self._paramType.columns * self._paramNumPerRow

    def _initGroupRows(self):
        """
        Group rows are the rows that contain the group buttons, which do
        not contain any parameters, and are used to fold and unfold the
        parameters below them.
        """
        for name in self._groupNames:
            self.insertRow(self.rowCount())
            self.setSpan(self.rowCount() - 1, 0, 1, self.columnCount())

            self._groupButtons[name] = FoldPushButton(name, self)
            self.params[name] = {}

            self.setCellWidget(self.rowCount() - 1, 0, self._groupButtons[name])

    def _insertParamRow(self, row_position):
        """
        Insert a row to the table after initialization.
        """
        # insert a row at row_position
        self.insertRow(row_position)
        # change the height of the row to 40
        self.setRowHeight(row_position, 50)
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
            # fix the width
            self.horizontalHeader().setSectionResizeMode(idx, QHeaderView.Fixed)
            width = self._paramType.columnWidths[entry_type]
            self.setHorizontalHeaderLabels(self._columns)
            self.setColumnWidth(idx, width)

        # disable the vertical header, grid, and frame
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setFrameShape(QTableWidget.NoFrame)

        # change the row height for group rows to 35
        for row in self._groupRows.values():
            self.setRowHeight(row, 35)

        # header height (same as row height for parameters)
        self.horizontalHeader().setFixedHeight(35)

    def _resizeTable(self):
        """
        Resize the table after the initialization. The hight is proportional
        to the number of rows plus the height of the header.
        """
        # fix the height of the table
        self.setMinimumHeight(
            (
                self.horizontalHeader().height()
                + np.sum([self.rowHeight(i) for i in range(self.rowCount())])
                + 2 * self.frameWidth()
                + self.horizontalScrollBar().height()
            )
        )

        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()

    def setWidthOfColumn(self):
        """
        Set the width of the columns.
        """
        for idx, entry_type in enumerate(self._columns):
            # fix the width
            width = self._paramType.columnWidths[entry_type]
            self.setColumnWidth(idx, width)

    def setHeightOfRow(self):
        """
        Set the height of the columns.
        """
        # for the group rows, set the height to 35
        for row in self._groupRows.values():
            self.setRowHeight(row, 35)
        # for the rest rows, set the height to 50
        for row in range(self.rowCount()):
            if row not in self._groupRows.values():
                self.setRowHeight(row, 50)
        self._resizeTable()

    def hideGroupLine(self):
        """
        Set the group line to be invisible.
        """
        for row in self._groupRows.values():
            self.setRowHeight(row, 0)
        self._resizeTable()

    def setCheckable(self, value):
        """
        Set the checkable property of the group buttons.
        """
        for button in self._groupButtons.values():
            # stop the button from emitting the signal
            button.setCheckable(value)
            button.blockSignals(not value)

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
        self.params[group][name] = self._paramType(self, name)

        # find the current section of the table
        group_row_idx = self._groupRows[group]

        # Since one parameter may occupy multiple columns, we need to
        # calculate the position of the parameter row / columns in the table.
        param_idx = len(self.params[group]) - 1  # which param
        param_row_idx = param_idx // self._paramNumPerRow
        param_column_idx = param_idx % self._paramNumPerRow

        current_row = param_row_idx + group_row_idx + 1  # +1 for the group row
        current_column = param_column_idx * self._paramType.columnCount

        # insert a row if it is the first parameter of a new row
        if param_column_idx == 0:
            self._insertParamRow(current_row)

        # insert the widgets
        for idx, entry_type in enumerate(self._paramType.columns):
            if self._paramType.columnBackgroundColors[entry_type] is not None:
                # Create an invisible table item for each cell, and set color
                # to the background color of the column.
                item = QTableWidgetItem()
                item.setBackground(
                    QColor(self._paramType.columnBackgroundColors[entry_type])
                )
                self.setItem(current_row, current_column + idx, item)
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
            group_lower_row = self._groupRows[
                self._groupNames[self._groupNames.index(group) + 1]
            ]
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
