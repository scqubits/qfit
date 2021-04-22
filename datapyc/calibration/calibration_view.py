# calibration_view.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide2.QtWidgets import QLineEdit, QMessageBox

from datapyc.core.helpers import DoubleValidator


class CalibrationView:
    def __init__(self, rawLineEdits, mapLineEdits):
        self.rawLineEdits = rawLineEdits
        self.mapLineEdits = mapLineEdits
        self.rawLineEdits["X1"].setSibling(self.rawLineEdits["X2"])
        self.rawLineEdits["Y1"].setSibling(self.rawLineEdits["Y2"])
        self.msg = None

    def calibrationErrorMsg(self):
        if self.msg is None:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("Calibration Error")
            self.msg.setInformativeText(
                "The two coordinate components used for calibration must not be identical."
            )
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
            self.msg = None

    def calibrationPoints(self):
        rVec1 = self.rawLineEdits["X1"].value(), self.rawLineEdits["Y1"].value()
        rVec2 = self.rawLineEdits["X2"].value(), self.rawLineEdits["Y2"].value()
        mVec1 = self.mapLineEdits["X1"].value(), self.mapLineEdits["Y1"].value()
        mVec2 = self.mapLineEdits["X2"].value(), self.mapLineEdits["Y2"].value()
        return rVec1, rVec2, mVec1, mVec2

    def setView(self, rawVec1, rawVec2, mapVec1, mapVec2):
        self.rawLineEdits["X1"].setText(str(rawVec1[0]))
        self.rawLineEdits["X2"].setText(str(rawVec2[0]))
        self.rawLineEdits["Y1"].setText(str(rawVec1[1]))
        self.rawLineEdits["Y2"].setText(str(rawVec2[1]))
        self.mapLineEdits["X1"].setText(str(mapVec1[0]))
        self.mapLineEdits["X2"].setText(str(mapVec2[0]))
        self.mapLineEdits["Y1"].setText(str(mapVec1[1]))
        self.mapLineEdits["Y2"].setText(str(mapVec2[1]))


class CalibrationLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(DoubleValidator())
        self.editingFinished.connect(self.processUpdate)
        self.previousStr = None
        self.siblingLineEdit = None

    def setSibling(self, siblingLineEdit):
        self.siblingLineEdit = siblingLineEdit

    def siblingValueDifferent(self):
        if not self.siblingLineEdit:
            return True
        return self.value() != self.siblingLineEdit.value()

    def focusOutEvent(self, arg):
        result = super().focusOutEvent(arg)
        self.processUpdate()
        return result

    def setText(self, arg):
        if self.previousStr is None:
            self.previousStr = arg
        try:
            _ = float(arg)
        except ValueError:
            arg = self.previousStr
        else:
            self.previousStr = arg
        super().setText(arg)

    def value(self):
        return float(self.text())

    def processUpdate(self):
        if self.hasAcceptableInput() and self.siblingValueDifferent():
            self.previousStr = self.text()
        else:
            self.setText(self.previousStr)
