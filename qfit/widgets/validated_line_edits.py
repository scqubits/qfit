# data_tagging.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from abc import ABC, abstractmethod

from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
from PySide6.QtGui import QValidator, QFocusEvent
from PySide6.QtWidgets import QLineEdit

from typing import Optional, Tuple, Union



# meta class for QLineEdits and ABC
class CombinedMeta(type(QLineEdit), type(ABC)):
    pass

class ValidatedLineEdit(QLineEdit, ABC, metaclass=CombinedMeta):
    """
    A base class for line edits that validate the input, if it's not valid
    the line edit is highlighted in red, and an error will 

    * A note to the developer: This class is a MV class, and the controller
    is also enbeded here.
    """

    _validator: QValidator
    _defaultStyle: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Model: Data and validation
        self._data: str = ""
        self._initializeValidator()

    # Model methods
    @abstractmethod
    def _initializeValidator(self, *args, **kwargs):
        """
        Initialize the validator for the line edit. This method should be
        overwritten by subclasses.
        """
        pass

    def isValid(self) -> bool:
        text = self.text()
        return (self.validator().validate(text, 0)[0] 
                == QValidator.State.Acceptable)

    # View methods
    def setInvalidStyle(self):
        self.setStyleSheet("border: 1.5px solid rgb(186, 40, 8);")

    def setDefaultStyle(self):
        self.setStyleSheet(self._defaultStyle)

    # Controller method
    def _validate(self):
        text = self.text()

        # when first called, record the current style as the default style
        if not hasattr(self, "_defaultStyle"):
            self._defaultStyle = self.styleSheet()

        if self.isValid():
            self._data = text
            self.setDefaultStyle()
        else:
            self.setInvalidStyle()

            # reset the text to the previous valid value
            # self.setText(self._data)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        """
        Handle the focus out event. Call the _validate method when the line edit loses focus.
        """
        super().focusOutEvent(event)
        self._validate()



# class StrTupleLineEdit(QLineEdit):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         regEx = QRegExp("(^[a-zA-Z][a-zA-Z0-9]*)+(, ?([a-zA-Z][a-zA-Z0-9]*)+)*$")
#         validator = QRegExpValidator(regEx)
#         self.setValidator(validator)

#         self.editingFinished.connect(self.processUpdate)
#         self.previousStr = ""

#     def setText(self, nameListStr):
#         if self.validator().validate(nameListStr, 0)[0] is QValidator.State.Acceptable:
#             self.previousStr = nameListStr
#         super().setText(nameListStr)

#     def value(self):
#         return self.text()

#     def getSubsysNameList(self):
#         if self.isValid():
#             return [name.strip() for name in self.value().split(",")]
#         return []

#     def setFromSubsysNameList(self, subsysNameList):
#         subsysStr = ", ".join(subsysNameList)
#         self.setText(subsysStr)

#     def subsysCount(self):
#         return len(self.getSubsysNameList())

#     def processUpdate(self):
#         if self.hasAcceptableInput():
#             self.previousStr = self.text()
#         else:
#             self.setText(self.previousStr)

#     def isValid(self):
#         return self.hasAcceptableInput()


class IntTupleLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts a tuple of integers as input, providing 
    validation and warning on invalid input.
    """

    # Model methods
    def _initializeValidator(self, tupleLength: Optional[int] = None):
        """
        Initialize the validator for the line edit. 
        When the tupleLength is not specified, the line edit accepts any
        number of integers separated by commas.
        """
        if tupleLength is None:
            regEx = QRegExp("^([1-9]\d*|0)(, ?([1-9]\d*|0))*$")
        else:
            regEx = QRegExp("^([1-9]\d*|0)(, ?([1-9]\d*|0)){%d}$" % (tupleLength - 1))
        self._validator = QRegExpValidator(regEx)
        self.setValidator(self._validator)

    def setTupleLength(self, tupleLength: int):
        self._initializeValidator(tupleLength)

    def getTuple(self) -> Union[Tuple[int, ...], None]:
        """
        Return the tuple of integers in the line edit.
        """
        if self.isValid():
            return tuple(int(x) for x in self.text().split(","))
        return None
    
    def setFromTuple(self, tuple_: Tuple[int, ...]):
        """
        Set the line edit from a tuple of integers.
        """
        self.setText(", ".join(str(x) for x in tuple_))
