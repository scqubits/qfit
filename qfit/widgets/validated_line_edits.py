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
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
from PySide6.QtGui import QValidator, QFocusEvent
from PySide6.QtWidgets import QLineEdit

from typing import Optional, Tuple, Union, List


# meta class for QLineEdits and ABC
class CombinedMeta(type(QLineEdit), type(ABC)):
    pass


class ValidatedLineEdit(QLineEdit, ABC, metaclass=CombinedMeta):
    """
    A base class for line edits that validate the input, if it's not valid
    the line edit is highlighted in red.

    * A note to the developer: This class is a MV class, and the controller
    is also enbeded here.
    """

    # view-level validator, prevent impossible characters from being entered
    # it will be set through the native instance.setValidator() method
    _validator: QValidator
    
    # model-level validator, check if the value is valid for the model
    # to accept it   
    _finalValidator: QValidator
    
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
        """
        Return whether the text in the line edit is valid on the MODEL level. 
        (or whether the text can be correctly parsed and accepted by the model)
        In contrast, isAcceptedByValidator() checks whether the text can
        be recognized by the validator. 
        
        isValid >= isAcceptedByValidator
        """
        text = self.text()
        return self._finalValidator.validate(text, 0)[0] == QValidator.State.Acceptable

    # View methods
    def isAcceptedByValidator(self) -> bool:
        """
        Return whether the text in the line edit is valid on the VIEW level.
        (or whether the text can is recognized by the validator).
        
        isValid >= isAcceptedByValidator
        """
        text = self.text()
        return self.validator().validate(text, 0)[0] == QValidator.State.Acceptable
    
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


class FloatLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts a float as input, providing validation and
    warning on invalid input.
    """

    def _initializeValidator(self):
        """
        Initialize the validator for the line edit.
        When the tupleLength is not specified, the line edit accepts any
        number of integers separated by commas.
        """
        self._validator = QDoubleValidator()
        self.setValidator(self._validator)

        self._finalValidator = self._validator
        

class PositiveFloatLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts a positive float as input, providing validation and
    warning on invalid input.
    """

    def _initializeValidator(self):
        """
        Initialize the validator for the line edit.
        When the tupleLength is not specified, the line edit accepts any
        number of integers separated by commas.
        """
        self._validator = QDoubleValidator()
        self._validator.setBottom(0)
        self.setValidator(self._validator)
        
        self._finalValidator = self._validator


class IntLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts an integer as input, providing validation and
    warning on invalid input.
    """

    def _initializeValidator(self):
        """
        Initialize the validator for the line edit.
        When the tupleLength is not specified, the line edit accepts any
        number of integers separated by commas.
        """
        self._validator = QIntValidator()
        self.setValidator(self._validator)

        self._finalValidator = self._validator
        
        



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
        
        # view-level validator: any possible partial input is accepted
        # e.g. ",2", "02, 3", "02, ,4"
        regEx = QRegExp("^[0-9,\s]*$")
        self._validator = QRegExpValidator(regEx)
        self.setValidator(self._validator)
        
        # model-level validator:
        if tupleLength is None:
            # integer tuple with any length
            regEx = QRegExp("^([1-9]\d*|0)(, ?([1-9]\d*|0))*$")
        else:
            # integer tuple with length tupleLength
            regEx = QRegExp("^([1-9]\d*|0)(, ?([1-9]\d*|0)){%d}$" % (tupleLength - 1))
        self._finalValidator = QRegExpValidator(regEx)

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


class StateLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts either a single integer or a tuple of integers
    """

    def _initializeValidator(self, tupleLength: Optional[int] = None):
        """
        Initialize the validator for the line edit.
        When the tupleLength is not specified, the line edit accepts any
        number of integers separated by commas.
        """
        
        # view-level validator: any possible partial input is accepted
        # e.g. "", "02", ",2", "02, 3", "02, ,4"
        regEx = QRegExp("^$|^[0-9,\s]*$")
        self._validator = QRegExpValidator(regEx)
        self.setValidator(self._validator)
        
        # model-level validator:
        if tupleLength is None:
            # integer tuple with any length or empty string
            regEx = QRegExp("^$|^([1-9]\d*|0)(, ?([1-9]\d*|0))*$")
        else:
            # integer or a tuple with length tupleLength or empty string
            num_commas = tupleLength - 1
            regEx = QRegExp(
                "^$|^([1-9]\d*|0)(, ?([1-9]\d*|0)){0,%d}$" % num_commas
            )
        self._finalValidator = QRegExpValidator(regEx)

    def setTupleLength(self, tupleLength: int):
        self._initializeValidator(tupleLength)

    def _isTuple(self) -> bool:
        """
        Return True if the line edit contains a tuple of integers.
        """
        return "," in self.text() and self.isValid()

    def _isInt(self) -> bool:
        """
        Return True if the line edit contains a single integer.
        """
        return not self._isTuple() and self.isValid()

    def getValue(self) -> Union[int, Tuple[int, ...], None]:
        """
        Return the value in the line edit. If the line edit contains a tuple,
        return a tuple of integers, otherwise return an integer.
        """
        if self._isTuple():
            return tuple(int(x) for x in self.text().split(","))
        elif self._isInt():
            return int(self.text())
        else:
            return None
        


class MultiIntsLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts semi-colon separated integers
    """
    def _initializeValidator(self):
        """
        Initialize the validators for the line edit.
        """
        # View-level validator: allows any partial input with digits, semicolons, and spaces
        viewRegEx = QRegExp("^[0-9;\s]*$")
        self._validator = QRegExpValidator(viewRegEx)
        self.setValidator(self._validator)

        # Model-level validator: ensures complete and valid input
        # Accepts any number of integers separated by semicolons
        modelRegEx = QRegExp("^$|^([1-9]\d*|0)(\s*;\s*([1-9]\d*|0))*$")
        
        self._finalValidator = QRegExpValidator(modelRegEx)
        
    def getInts(self) -> List[int | None]:
        """
        Return the integers in the line edit.
        """
        if not self.isValid():
            return [None]

        ints = []
        for int_str in self.text().split(";"):
            if int_str.strip() == "":
                ints.append(None)
            else:
                ints.append(int(int_str))
                
        assert not (None in ints and len(ints) > 1), "Impossible case, " \
            "which should be already caught by the validator"  
        
        return ints
    
    def setFromInts(self, ints: List[int | None]):
        strs = []
        for int_ in ints:
            if int_ is None:
                strs.append("")
            else:   
                strs.append(str(int_))
        self.setText("; ".join(strs))


class MultiIntTuplesLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts semi-colon separated tuples of integers, where each tuple
    has a specified length.
    """
    def _initializeValidator(self, tupleLength: Optional[int] = None):
        """
        Initialize the validators for the line edit.
        """
        # View-level validator: allows any partial input with digits, commas, semicolons, and spaces
        viewRegEx = QRegExp("^[0-9,;\s]*$")
        self._validator = QRegExpValidator(viewRegEx)
        self.setValidator(self._validator)

        # Model-level validator: ensures complete and valid input
        if tupleLength is None:
            # Accepts any number of tuples, each being a tuple of any length
            modelRegEx = QRegExp("^$|^([1-9]\d*|0)(\s*,\s*([1-9]\d*|0))*"
                                 "(\s*;\s*([1-9]\d*|0)(\s*,\s*([1-9]\d*|0))*)*$")
        else:
            # Accepts any number of tuples, each being a tuple with the specified length
            num_commas = tupleLength - 1
            modelRegEx = QRegExp("^$|^([1-9]\d*|0)(\s*,\s*([1-9]\d*|0)){%d}"
                                 "(\s*;\s*([1-9]\d*|0)(\s*,\s*([1-9]\d*|0)){%d})*$" % (num_commas, num_commas))
        
        self._finalValidator = QRegExpValidator(modelRegEx)
        
    def setTupleLength(self, tupleLength: int):
        self._initializeValidator(tupleLength)
        
    def getTuples(self) -> List[Tuple[int, ...] | None]:
        """
        Return the tuples in the line edit. Each tuple is a tuple of integers.
        """
        if not self.isValid():
            return [None]
        
        tuples = []
        for tuple_str in self.text().split(";"):
            if tuple_str.strip() == "":
                tuples.append(None)
            else:
                tuples.append(tuple(int(x) for x in tuple_str.split(",")))
                
        assert not (None in tuples and len(tuples) > 1), "Impossible case, " \
            "which should be already caught by the validator"  
        
        return tuples
    
    def setFromTuples(self, tuples: List[Tuple[int, ...] | None]):
        strs = []
        for tuple_ in tuples:
            if tuple_ is None:
                strs.append("")
            else:   
                strs.append(", ".join(str(x) for x in tuple_))
        self.setText("; ".join(strs))


class MultiStatesLineEdit(ValidatedLineEdit):
    """
    A line edit that accepts semi-colon separated states, where each state
    is either a single integer or a tuple of integers with a specified length
    (each element is the same as StateLineEdit)
    """

    def _initializeValidator(self, tupleLength: Optional[int] = None):
        """
        Initialize the validators for the line edit.
        """
        # View-level validator: allows any partial input with digits, commas, semicolons, and spaces
        viewRegEx = QRegExp("^[0-9,;\s]*$")
        self._validator = QRegExpValidator(viewRegEx)
        self.setValidator(self._validator)

        # Model-level validator: ensures complete and valid input
        if tupleLength is None:
            # Accepts any number of states, each being an int or a tuple of any length
            modelRegEx = QRegExp("^$|^([1-9]\d*|0)(\s*,\s*([1-9]\d*|0))*"
                                 "(\s*;\s*([1-9]\d*|0)(\s*,\s*([1-9]\d*|0))*)*$")
        else:
            # Accepts any number of states, each being an int or a tuple with the specified length
            num_commas = tupleLength - 1
            modelRegEx = QRegExp("^$|^([1-9]\d*|0)(\s*,\s*([1-9]\d*|0)){0,%d}"
                                 "(\s*;\s*([1-9]\d*|0)(\s*,\s*([1-9]\d*|0)){0,%d})*$" % (num_commas, num_commas))
        
        self._finalValidator = QRegExpValidator(modelRegEx)
        
    def setTupleLength(self, tupleLength: int):
        self._initializeValidator(tupleLength)
        
    def getStates(self) -> List[int | Tuple[int, ...] | None]:
        """
        Return the states in the line edit. Each state is either an integer or a tuple of integers.
        """
        if not self.isValid():
            return [None]
        
        states = []
        for state in self.text().split(";"):
            if state.strip() == "":
                states.append(None)
            elif "," in state:
                states.append(tuple(int(x) for x in state.split(",")))
            else:
                states.append(int(state))
        return states

