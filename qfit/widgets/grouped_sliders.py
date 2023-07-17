from PySide6.QtWidgets import (
    QSlider, 
    QLineEdit, 
    QLabel, 
    QWidget, 
    QGridLayout
)
from PySide6.QtCore import Qt

class LabeledSlider(QWidget):
    """A widget that contains a slider as well as its name and value as QLineEdit."""
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
        
        # connect the slider to the value line edit
        self.slider.valueChanged.connect(self.updateValue)
        self.value.textChanged.connect(self.updateSlider)

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
    
    def updateValue(self, value):
        self.value.setText(str(value))
        
    def updateSlider(self, value):
        if value.isdigit():
            self.slider.setValue(int(value))



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