from PySide6.QtWidgets import (
    QSlider, 
    QLineEdit, 
    QLabel, 
    QWidget, 
    QGridLayout,
    QVBoxLayout,
    QGroupBox
)
from PySide6.QtCore import Qt

from typing import Dict, List, Tuple, Union

class LabeledSlider(QWidget):
    """A widget that contains a slider as well as its name and value as QLineEdit."""
    user_is_sliding = False

    def __init__(
        self, 
        label_text='Slider', 
        label_value_position='left_right', 
        parent=None
    ):
        super().__init__(parent)
        
        # initialize the widgets
        self.label = QLabel(label_text, self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.value = QLineEdit("0", self)
        self.value.setMaximumWidth(50)

        # initialize the layout
        self.sliderLayout = QGridLayout(self)

        # insert the widgets into the layout
        self._insertWidgets(label_value_position)

        # connect the widgets
        self.slider.sliderPressed.connect(self.sliderPressed)
        self.slider.sliderReleased.connect(self.sliderReleased)

    def _insertWidgets(self, label_value_position):
        """add the widgets to the layout according to the label_value_position"""
        if label_value_position == 'left_right':
            slider_position = (0, 1)
            label_position = (0, 0)
            value_position = (0, 2)
        elif label_value_position == 'right_left':
            slider_position = (0, 1)
            label_position = (0, 2)
            value_position = (0, 0)
        elif label_value_position == 'both_bottom':
            slider_position = (0, 0, 1, 2)
            label_position = (1, 0)
            value_position = (1, 1)
        else:
            raise ValueError(f"Unknown label_value_position: {label_value_position}")
        
        self.sliderLayout.addWidget(self.slider, *slider_position)
        self.sliderLayout.addWidget(self.label, *label_position)
        self.sliderLayout.addWidget(self.value, *value_position)

    def sliderPressed(self):
        self.user_is_sliding = True

    def sliderReleased(self):
        self.user_is_sliding = False

    def sliderValueChangedConnect(self, func):
        """
        Make the slider only call the function when the user is sliding. 

        The value box will update the slider value, but will not call the function.
        """
        def func_wrapper(*args, **kwargs):
            if self.user_is_sliding:
                func(*args, **kwargs)
        self.slider.valueChanged.connect(func_wrapper)

    def valueTextChangeConnect(self, func):
        """
        Just make things consistent. 
        """
        self.value.textChanged.connect(func)
    

class GroupedSliders(QWidget):
    def __init__(
        self, 
        slider_names, 
        columns=2, 
        label_value_position='left_right', 
        parent=None
    ):
        super().__init__(parent)
        
        self.gridLayout = QGridLayout(self)
        self.sliders = {}
        self.columns = columns
        self.label_value_position = label_value_position

        self.createSliders(slider_names)

    def keys(self):
        return self.sliders.keys()
    
    def values(self):
        return self.sliders.values()
    
    def items(self):
        return self.sliders.items()
    
    def __getitem__(self, key) -> LabeledSlider:
        return self.sliders[key]

    def createSliders(self, slider_names):
        # Clear existing sliders
        self.clearLayout()

        for idx, name in enumerate(slider_names):
            slider = LabeledSlider(label_text=name, label_value_position=self.label_value_position)
            self.sliders[name] = slider
            self.gridLayout.addWidget(slider, idx // self.columns, idx % self.columns)
            
    def clearLayout(self):
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.sliders.clear()


class FoldableWidget(QGroupBox):
    def __init__(self, title='Foldable', content_widget=None, parent=None):
        super().__init__(parent)

        self.setTitle(title)
        self.setCheckable(True)

        self.boxLayout = QVBoxLayout(self)
        self.content_widget = content_widget if content_widget else QLabel("No Content", self)
        self.boxLayout.addWidget(self.content_widget)

        self.setChecked(False)
        self.toggleContent(self.isChecked())
        self.toggled.connect(self.toggleContent)

    def toggleContent(self, checked):
        self.content_widget.setVisible(checked)

    def setConentWidget(self, content_widget):
        # remove
        self.boxLayout.removeWidget(self.content_widget)

        # add
        self.content_widget = content_widget
        self.boxLayout.addWidget(self.content_widget)


class GroupedSliderSet(QWidget):
    def __init__(
        self, 
        columns=2, 
        label_value_position='left_right',
        parent=None
    ):
        super().__init__(parent)

        self.sliderSetParent = parent
        self.columns = columns
        self.labelValuePosition = label_value_position

        self.sliderSetLayout = QVBoxLayout(self)
        self.slider_groups: Dict[str, GroupedSliders] = {}

    def keys(self):
        return self.slider_groups.keys()
    
    def values(self):
        return self.slider_groups.values()
    
    def items(self):
        return self.slider_groups.items()
    
    def __getitem__(self, key):
        return self.slider_groups[key]
    
    def addGroupedSliders(
        self, 
        set_name: str, 
        slider_names: List[str], 
    ):
        # store the sliders
        self.slider_groups[set_name] = GroupedSliders(
            slider_names, 
            columns=self.columns, 
            label_value_position=self.labelValuePosition,
            parent=self.sliderSetParent,
        )

        # add the sliders to the layout
        self.sliderSetLayout.addWidget(FoldableWidget(
            set_name,
            self.slider_groups[set_name],
        ))

    
