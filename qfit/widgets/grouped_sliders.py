from PySide6.QtWidgets import (
    QSlider,
    QLineEdit,
    QLabel,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from qfit.utils.helpers import modifyStyleSheet

from qfit.widgets.foldable_widget import (
    FoldableWidget,
    SPACING,
)
from qfit.widgets.validated_line_edits import FloatLineEdit

from typing import Dict, List, Tuple, Union, Optional, Any, TypeVar, Generic, Type

SLIDER_RANGE = 100
SPACING_BETWEEN_GROUPS = 15
MARGIN = 12


class LabeledSlider(QWidget):
    """
    A widget that contains a slider as well as its name and value as QLineEdit.

    When user are using either the slider or the value box, functions can be set
    to achieve that the other one will be updated accordingly. Endless call loops will
    be avoided if using the provided methods.

    Parameters
    ----------
    name : str
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
        self._label = QLabel(name)
        self._slider = QSlider(Qt.Horizontal, self)
        self._slider.setMinimum(1)
        self._slider.setMaximum(SLIDER_RANGE)
        self._slider.setSingleStep(1)
        self._textBox = FloatLineEdit("0", self)
        self._textBox.setMaximumWidth(50)

        # format the widgets
        self._formatLabeledSlider()

        # initialize the layout
        self._sliderLayout = QGridLayout(self)

        # insert the widgets into the layout
        self._insertWidgets(label_value_position)

        # connect the widgets
        # This is the most important part of this class. We assume the slider and the value
        # will later be connected by the user. This class will keep track of the user's
        # behavior and avoid endless call loops, realized by the following connections.
        self._slider.sliderPressed.connect(self._userSliding)
        self._slider.sliderReleased.connect(self._userSlidingEnds)
        self._textBox.textChanged.connect(self._userTyping)
        self._textBox.editingFinished.connect(self._userTypingEnds)

        # margin and spacing
        self._sliderLayout.setContentsMargins(0, 0, 0, 0)
        self._sliderLayout.setSpacing(SPACING)

        # connect the slider and the value box in a simplest way
        if auto_connect:
            self._naiveConnection()

    def _insertWidgets(self, label_value_position):
        """
        Insert the slider, label, and value box into the layout according to the
        label_value_position.

        Parameters
        ----------
        label_value_position : str
            The position of the label and the value box.
            - 'left_right': label, slider, value
            - 'right_left': slider, label, value
            - 'both_bottom': slider, (line break), label, value
            - 'value_left': slider, value
            - 'value_right': value, slider
        """
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
            self._sliderLayout.addWidget(self._slider, *slider_position)
        self._sliderLayout.addWidget(self._label, *label_position)
        self._sliderLayout.addWidget(self._textBox, *value_position)

    def _naiveConnection(self):
        """
        The simplest way to connect the slider and the value box:
        - the value box displays the raw value of the slider.
        - the slider value is set to the value box when the value box is changed.
        """
        def updateValue():
            self._textBox.setText(str(self._slider.value()))

        def updateSlider():
            self._slider.setValue(int(self._textBox.text()))

        self.sliderValueChangedConnect(updateValue)
        self.textValueChangedConnect(updateSlider)

    def _userSliding(self):
        """
        Set the flag to indicate that the user is sliding the slider,
        it's used to avoid endless call loops.
        """
        self.user_is_sliding = True

    def _userSlidingEnds(self):
        """
        Set the flag to indicate that the user is done sliding the slider,
        it's used to avoid endless call loops.
        """
        self.user_is_sliding = False

    def _userTyping(self):
        """
        Set the flag to indicate that the user is typing in the value box,
        it's used to avoid endless call loops.
        """
        if not self.user_is_sliding:
            self.user_is_typing = True
        else:
            self.user_is_typing = False

    def _userTypingEnds(self):
        """
        Set the flag to indicate that the user is done typing in the value box,
        it's used to avoid endless call loops.
        """
        self.user_is_typing = False

    def _formatLabeledSlider(self):
        """
        Format the labeled slider.
        """
        modifyStyleSheet(self._textBox, "border", "1px solid #5F5F5F")
        modifyStyleSheet(self._textBox, "font", '13px "Roboto Medium"')
        modifyStyleSheet(self._textBox, "color", "#FFFFFF")
        modifyStyleSheet(self._label, "font", '13px "Roboto Medium"')
        modifyStyleSheet(self._label, "color", "#FFFFFF")

    def setEnabled(self, value: bool) -> None:
        self._slider.setEnabled(value)
        self._textBox.setEnabled(value)

    # public methods
    def sliderValueChangedConnect(self, func):
        """
        Should be used instead of self._slider.valueChanged.connect(func).

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

        self._slider.valueChanged.connect(func_wrapper)

    def textValueChangedConnect(self, func):
        """
        Should be used instead of self._textBox.textChanged.connect(func).

        Both user and (potentially) slider value change will emit the value.textChanged
        signal. This function will react to the signal only when the user is typing
        (not sliding). It will also avoid endless call loops.
        """

        def func_wrapper(*args, **kwargs):
            if self.user_is_typing and not self.user_is_sliding:
                func(*args, **kwargs)

        self._textBox.textChanged.connect(func_wrapper)

    def editingFinishedConnect(self, func):
        """
        Emit the signal when the user is done typing / sliding.
        Should be used instead of self._textBox.editingFinished.connect(func).
        """
        # remove the last connection, which is always self.editingFinished
        self._textBox.editingFinished.disconnect(self._userTypingEnds)

        # connect
        self._textBox.editingFinished.connect(func)
        self._slider.sliderReleased.connect(func)

        # put the self.editingFinished back
        self._textBox.editingFinished.connect(self._userTypingEnds)

    def setValue(self, value: Union[str, int], toSlider: bool = True):
        """
        A wrapper of self.value.setText() that will NOT trigger any signals.
        """
        if toSlider:
            self._slider.setValue(int(value))
        else:
            self.user_is_typing = False
            self._textBox.setText(value)
            self.user_is_typing = False



WidgetCls = TypeVar("WidgetCls", bound=QWidget)


class GroupedWidget(QWidget, Generic[WidgetCls]):
    """
    A class that contains multiple widgets, which will be displayed in a grid layout.

    Parameters
    ----------
    widgetClass : QWidget
        The class of the widget to be grouped. The initialization of the widget should
        accept a name as it's first positional argument (even if the name is not displayed).
    widgetNames : List[str]
        The names of the widgets to be grouped.
    initKwargs : Dict[str, Any]
        The keyword arguments to be passed to the initialization of the widget.
    columns : int
        The number of columns in the grid layout.
    parent : QWidget
    """

    def __init__(
        self,
        widgetClass: Type[WidgetCls],
        widgetNames: List[str],
        initKwargs: Dict[str, Any] = {},
        columns: int = 2,
        parent = None,
    ):
        super().__init__(parent)

        self.widgetClass = widgetClass
        self.widgets: Dict[str, WidgetCls] = {}
        self.initKwargs = initKwargs

        self.columns = columns
        self.gridLayout = QGridLayout(self)

        self.insertMultipleWidgets(widgetNames)

        # set the layout that no vertical space between the widgets (labelled sliders here)
        self.gridLayout.setContentsMargins(MARGIN, 0, MARGIN, 0)

        # self.gridLayout.setVerticalSpacing(SPACING_BETWEEN_SLIDERS)

    def keys(self):
        return self.widgets.keys()

    def values(self):
        return self.widgets.values()

    def items(self):
        return self.widgets.items()

    def __getitem__(self, key):
        return self.widgets[key]
    
    def insertWidget(self, name: str, idx: Optional[int] = None):
        """
        Insert a widget into the layout.
        """
        if idx is None:
            idx = len(self.widgets)
        widget = self.widgetClass(name, **self.initKwargs)
        self.widgets[name] = widget
        self.gridLayout.addWidget(widget, idx // self.columns, idx % self.columns)

    def removeWidget(self, name: str):
        """
        Remove a widget from the layout.
        """
        widget = self.widgets.pop(name)
        widget.setParent(None)
        del widget

    def insertMultipleWidgets(self, widget_names: List[str]):
        """
        Insert multiple widgets into the layout based on the given names.
        """
        # Clear existing sliders
        self.clearLayout()

        for idx, name in enumerate(widget_names):
            self.insertWidget(name, idx)

    def clearLayout(self):
        """
        Remove all the widgets from the layout.
        """
        for widget in self.widgets.values():
            self.removeWidget(widget)

    def setEnabled(self, value):
        for widget in self.values():
            widget.setEnabled(value)


class GroupedWidgetSet(QWidget, Generic[WidgetCls]):
    """
    Multiple GroupedWidget instances, which will be displayed in a vertical layout.

    Parameters
    ----------
    widgetClass : QWidget
        The class of the widget to be grouped. The initialization of the widget should
        accept a name as it's first positional argument (even if the name is not displayed).
    initKwargs : Dict[str, Any]
        The keyword arguments to be passed to the initialization of the widget.
    columns : int
        The number of columns in the grid layout.
    parent : QWidget
    """

    def __init__(
        self, 
        widgetClass: Type[WidgetCls], 
        initKwargs: Dict[str, Any] = {}, 
        columns = 2, 
        parent = None
    ):
        super().__init__(parent)

        self.widgetClass = widgetClass
        self.initKwargs = initKwargs

        self.columns = columns
        self.widgetSetLayout = QVBoxLayout(self)
        self.widgetSetLayout.setContentsMargins(0, 0, 0, 0)  # Remove the margins
        self.widgetSetLayout.setSpacing(SPACING_BETWEEN_GROUPS)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.widgetGroups: Dict[str, GroupedWidget] = {}

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
        setName: str,
        widgetNames: List[str],
    ):
        """
        Add a group of widgets to the layout, it will automatically create a GroupedWidget
        instance and add it to the layout.

        Parameters
        ----------
        setName : str
            The name of the group.
        widgetNames : List[str]
            The names of the widgets to be grouped, one of the parameters of 
            the widgetClass.
        """
        # store the group
        self.widgetGroups[setName] = GroupedWidget(
            widgetClass=self.widgetClass,
            widgetNames=widgetNames,
            initKwargs=self.initKwargs,
            columns=self.columns,
            parent=self,
        )

        # add the group to the layout
        self.widgetSetLayout.addWidget(
            FoldableWidget(
                setName,
                self.widgetGroups[setName],
            )
        )

    def removeGroupedWidgets(self, set_name: str):
        """
        Remove a group of widgets from the layout.
        """
        self.widgetSetLayout.removeWidget(self.widgetGroups[set_name])
        self.widgetGroups[set_name].setParent(None)
        del self.widgetGroups[set_name]

    def setEnabled(self, value):
        for group in self.values():
            group.setEnabled(value)

