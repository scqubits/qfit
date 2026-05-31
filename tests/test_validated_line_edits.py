"""Tests for validated line edit widgets (pattern W)."""
import pytest

from qfit.widgets.validated_line_edits import (
    FloatLineEdit,
    IntLineEdit,
    MultiIntsLineEdit,
)


pytestmark = [pytest.mark.gui, pytest.mark.unit]


class TestFloatLineEdit:
    def test_valid_float(self, qtbot):
        w = FloatLineEdit()
        qtbot.addWidget(w)
        w.setText("1.23")
        assert w.isValid()

    def test_invalid_text(self, qtbot):
        w = FloatLineEdit()
        qtbot.addWidget(w)
        w.setText("abc")
        assert not w.isValid()


class TestIntLineEdit:
    def test_valid_int(self, qtbot):
        w = IntLineEdit()
        qtbot.addWidget(w)
        w.setText("42")
        assert w.isValid()


class TestMultiIntsLineEdit:
    def test_valid_list(self, qtbot):
        w = MultiIntsLineEdit()
        qtbot.addWidget(w)
        w.setText("1; 2; 3")
        assert w.isValid()

    def test_invalid_list(self, qtbot):
        w = MultiIntsLineEdit()
        qtbot.addWidget(w)
        w.setText("1, x")
        assert not w.isValid()
