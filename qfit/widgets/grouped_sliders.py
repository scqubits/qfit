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

from typing import Dict, List, Tuple, Union, Optional, Any

SLIDER_RANGE = 100


class LabeledSlider(QWidget):
    """
    A widget that contains a slider as well as its name and value as QLineEdit.

    When user are using either the slider or the value box, functions can be set
    to achieve that the other one will be updated accordingly. Endless call loops will
    be avoided if using the provided methods.

    Parameters
    ----------
    label_text : str
        The name of the slider, will be displayed as a QLabel.
    label_value_position : str
        The position of the label and the value box.
        - 'left_right': label, slider, value
        - 'right_left': slider, label, value
        - 'both_bottom': slider, (line break), label, value
        - 'value_left': slider, value
        - 'value_right': value, slider
    auto_connect : bool
        If True, the slider and the value box will be connected in a simplest way: box displays
        the raw value of the slider.
    parent : QWidget
        The parent widget.
    """

    user_is_sliding = False
    user_is_typing = False

    def __init__(
        self,
        name: str = "Slider",
        label_value_position: str = "left_right",
        auto_connect: bool = False,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # initialize the widgets
        self.label = QLabel(name)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(SLIDER_RANGE)
        self.slider.setSingleStep(1)
        self.value = QLineEdit("0", self)
        self.value.setMaximumWidth(50)

        # initialize the layout
        self.sliderLayout = QGridLayout(self)

        # insert the widgets into the layout
        self._insertWidgets(label_value_position)

        # connect the widgets
        # This is the most important part of this class. We assume the slider and the value
        # will later be connected by the user. This class will keep track of the user's
        # behavior and avoid endless call loops, realized by the following connections.
        self.slider.sliderPressed.connect(self._userSliding)
        self.slider.sliderReleased.connect(self._userSlidingEnds)
        self.value.textChanged.connect(self._userTyping)
        self.value.editingFinished.connect(self._userTypingEnds)

        # connect the slider and the value box in a simplest way
        if auto_connect:
            self._naiveConnection()

    def _insertWidgets(self, label_value_position):
        """add the widgets to the layout according to the label_value_position"""
        with_label = label_value_position in ["left_right", "right_left", "both_bottom"]

        if label_value_position == "left_right":
            slider_position = (0, 1)
            label_position = (0, 0)
            value_position = (0, 2)
        elif label_value_position == "right_left":
            slider_position = (0, 1)
            label_position = (0, 2)
            value_position = (0, 0)
        elif label_value_position == "both_bottom":
            slider_position = (0, 0, 1, 2)
            label_position = (1, 0)
            value_position = (1, 1)
        elif label_value_position == "value_left":
            slider_position = (0, 1)
            label_position = None
            value_position = (0, 0)
        elif label_value_position == "value_right":
            slider_position = (0, 0)
            label_position = None
            value_position = (0, 1)
        else:
            raise ValueError(f"Unknown label_value_position: {label_value_position}")

        if with_label:
            self.sliderLayout.addWidget(self.slider, *slider_position)
        self.sliderLayout.addWidget(self.label, *label_position)
        self.sliderLayout.addWidget(self.value, *value_position)

    def _naiveConnection(self):
        """
        The simplest way to connect the slider and the value box.
        """

        def updateValue():
            self.value.setText(str(self.slider.value()))

        def updateSlider():
            self.slider.setValue(int(self.value.text()))

        self.sliderValueChangedConnect(updateValue)
        self.valueTextChangeConnect(updateSlider)

    def _userSliding(self):
        self.user_is_sliding = True

    def _userSlidingEnds(self):
        self.user_is_sliding = False

    def _userTyping(self):
        if not self.user_is_sliding:
            self.user_is_typing = True
        else:
            self.user_is_typing = False

    def _userTypingEnds(self):
        self.user_is_typing = False

    def sliderValueChangedConnect(self, func):
        """
        Both user and (potentially) box value change will emit the slider.valueChanged
        signal. This function will react to the signal only when the user is sliding
        (not typing). It will also avoid endless call loops.
        """

        def func_wrapper(*args, **kwargs):
            # when user is sliding
            if self.user_is_sliding and not self.user_is_typing:
                func(*args, **kwargs)
            # when user just clicked the slider and change the value
            elif not self.user_is_sliding and not self.user_is_typing:
                self.user_is_sliding = True
                func(*args, **kwargs)
                self.user_is_sliding = False

        self.slider.valueChanged.connect(func_wrapper)

    def valueTextChangeConnect(self, func):
        """
        Both user and (potentially) slider value change will emit the value.textChanged
        signal. This function will react to the signal only when the user is typing
        (not sliding). It will also avoid endless call loops.
        """

        def func_wrapper(*args, **kwargs):
            if self.user_is_typing and not self.user_is_sliding:
                func(*args, **kwargs)

        self.value.textChanged.connect(func_wrapper)

    def editingFinishedConnect(self, func):
        """
        Emit the signal when the user is done typing / sliding.
        """

        # remove the last connection, which is always self.editingFinished
        self.value.editingFinished.disconnect(self._userTypingEnds)

        # connect
        self.value.editingFinished.connect(func)
        self.slider.sliderReleased.connect(func)

        # put the self.editingFinished back
        self.value.editingFinished.connect(self._userTypingEnds)

    def setValue(self, value: str):
        """
        A wrapper of self.value.setText() that will NOT trigger any signals.
        """
        self.user_is_typing = False
        self.value.setText(value)
        self.user_is_typing = False


class GroupedWidget(QWidget):
    """
    A class that contains multiple LabeledSlider widgets. The sliders will be displayed
    in a grid layout.

    Parameters
    ----------
    widget_class : QWidget
        The class of the widget to be grouped. The initialization of the widget should
        accept a name as it's first positional argument (even if the name is not displayed).
    widget_names : List[str]
        The names of the widgets to be grouped.
    init_kwargs : Dict[str, Any]
        The keyword arguments to be passed to the initialization of the widget.
    columns : int
        The number of columns in the grid layout.
    parent : QWidget
    """

    def __init__(
        self,
        widget_class,
        widget_names: List[str],
        init_kwargs: Dict[str, Any] = {},
        columns: int = 2,
        parent=None,
    ):
        super().__init__(parent)

        self.widget_class = widget_class
        self.widgets = {}
        self.init_kwargs = init_kwargs

        self.columns = columns
        self.gridLayout = QGridLayout(self)

        self.createWidgets(widget_names)
        # set the layout that no vertical space between the widgets (labelled sliders here)
        self.gridLayout.setVerticalSpacing(0)

    def keys(self):
        return self.widgets.keys()

    def values(self):
        return self.widgets.values()

    def items(self):
        return self.widgets.items()

    def __getitem__(self, key):
        return self.widgets[key]

    def createWidgets(self, widget_names):
        # Clear existing sliders
        self.clearLayout()

        for idx, name in enumerate(widget_names):
            widget = self.widget_class(name, **self.init_kwargs)
            self.widgets[name] = widget
            self.gridLayout.addWidget(widget, idx // self.columns, idx % self.columns)

    def clearLayout(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.widgets.clear()


class FoldableWidget(QGroupBox):
    """
    A widget that contains a title and a content widget. The content widget will be
    hidden when the widget is not checked.
    """

    def __init__(self, title="Foldable", content_widget=None, parent=None):
        super().__init__(parent)
        # set fold push button
        self.foldPushButton = QPushButton(self)
        self.setObjectName("foldPushButton")
        # icon
        icon = QIcon()
        icon.addFile(
            ":/icons/16x16/cil-caret-right.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon.addFile(
            ":/icons/16x16/cil-caret-bottom.png",
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        # set the style sheet (which controls the font, color, text align, border, etc.)
        self.foldPushButton.setStyleSheet(
            "QPushButton {\n"
            '	font: 57 10pt "Roboto Medium";\n'
            "	color: rgb(170, 170, 170);\n"
            "	text-align: left;\n"
            "	border: none;\n"
            "}"
        )
        self.foldPushButton.setIcon(icon)
        # set title
        self.foldPushButton.setText(
            QCoreApplication.translate("MainWindow", title, None)
        )
        # set checkable
        self.foldPushButton.setCheckable(True)
        self.foldPushButton.setChecked(False)

        # set the box layout
        self.boxLayout = QVBoxLayout(self)
        # add push button to the layout
        self.boxLayout.addWidget(self.foldPushButton)
        # add content widget
        self.content_widget = (
            content_widget if content_widget else QLabel("No Content", self)
        )
        self.boxLayout.addWidget(self.content_widget)

        # connect the push button to the setVisible method
        self.foldPushButton.clicked.connect(
            lambda: self.toggleContent(self.foldPushButton.isChecked())
        )
        # initialize the content
        self.toggleContent(self.foldPushButton.isChecked())
        # set the size policy for the foldable widget: expand along horizontal, fixed along vertical
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def toggleContent(self, checked):
        self.content_widget.setVisible(checked)

    def setConentWidget(self, content_widget):
        # remove
        self.boxLayout.removeWidget(self.content_widget)

        # add
        self.content_widget = content_widget
        self.boxLayout.addWidget(self.content_widget)


class GroupedWidgetSet(QWidget):
    """
    Represent a set of grouped sliders. Each group will be displayed in a FoldableWidget.
    """

    def __init__(
        self, widget_class, init_kwargs: Dict[str, Any] = {}, columns=2, parent=None
    ):
        super().__init__(parent)

        self.widget_class = widget_class
        self.init_kwargs = init_kwargs

        self.columns = columns
        self.widgetSetLayout = QVBoxLayout(self)
        self.widgetSetLayout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.widgetSetLayout.setObjectName("WidgetSetLayout")
        # self.widgetSetLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetGroups: Dict[str, Any] = {}

    def keys(self):
        return self.widgetGroups.keys()

    def values(self):
        return self.widgetGroups.values()

    def items(self):
        return self.widgetGroups.items()

    def __getitem__(self, key):
        return self.widgetGroups[key]

    def addGroupedWidgets(
        self,
        set_name: str,
        widget_names: List[str],
    ):
        # store the group
        self.widgetGroups[set_name] = GroupedWidget(
            widget_class=self.widget_class,
            widget_names=widget_names,
            init_kwargs=self.init_kwargs,
            columns=self.columns,
            parent=self,
        )

        # add the group to the layout
        self.widgetSetLayout.addWidget(
            FoldableWidget(
                set_name,
                self.widgetGroups[set_name],
            )
        )


class FittingParameterRow(QWidget):
    """
    A collection of widgets that represents a row in the FittingParameterTable.
    """

    entry_types = ["Name", "Fix", "Initial", "Current", "Min", "Max"]

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

        # configure the table layout
        self.configure()

        # insert the rows
        self.parameterWidgets: Dict[str, FittingParameterRow] = {}
        for name in row_names:
            self.insertParameter(name)

    def configure(self):
        # Set the column widths.
        for idx, entry_type in enumerate(self.columns):
            width = 40 if entry_type in ["Name", "Fix"] else 60
            self.setColumnWidth(idx, width)

        # configure
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.horizontalHeader().setStyleSheet("color: white")

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
