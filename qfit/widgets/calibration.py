# calibration.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide6.QtWidgets import QMessageBox

from qfit.widgets.validated_line_edits import FloatLineEdit


class CalibrationView:
    def __init__(self, rawLineEdits, mapLineEdits):
        self.rawLineEdits = rawLineEdits
        self.mapLineEdits = mapLineEdits
        self.rawLineEdits["CALI_X1"].setSibling(self.rawLineEdits["CALI_X2"])
        self.rawLineEdits["CALI_Y1"].setSibling(self.rawLineEdits["CALI_Y2"])
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
        rVec1 = self.rawLineEdits["CALI_X1"].value(), self.rawLineEdits["CALI_Y1"].value()
        rVec2 = self.rawLineEdits["CALI_X2"].value(), self.rawLineEdits["CALI_Y2"].value()
        mVec1 = self.mapLineEdits["CALI_X1"].value(), self.mapLineEdits["CALI_Y1"].value()
        mVec2 = self.mapLineEdits["CALI_X2"].value(), self.mapLineEdits["CALI_Y2"].value()
        return rVec1, rVec2, mVec1, mVec2

    def setView(self, rawVec1, rawVec2, mapVec1, mapVec2):
        self.rawLineEdits["CALI_X1"].setText(str(rawVec1[0]))
        self.rawLineEdits["CALI_X2"].setText(str(rawVec2[0]))
        self.rawLineEdits["CALI_Y1"].setText(str(rawVec1[1]))
        self.rawLineEdits["CALI_Y2"].setText(str(rawVec2[1]))
        self.mapLineEdits["CALI_X1"].setText(str(mapVec1[0]))
        self.mapLineEdits["CALI_X2"].setText(str(mapVec2[0]))
        self.mapLineEdits["CALI_Y1"].setText(str(mapVec1[1]))
        self.mapLineEdits["CALI_Y2"].setText(str(mapVec2[1]))


class CalibrationLineEdit(FloatLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.editingFinished.connect(self.processUpdate)
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
        # self.processUpdate()
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

    # def processUpdate(self):
    #     if self.hasAcceptableInput() and self.siblingValueDifferent():
    #         self.previousStr = self.text()
    #     else:
    #         self.setText(self.previousStr)
