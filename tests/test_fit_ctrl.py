"""Smoke tests for FitCtrl."""
import pytest


pytestmark = [pytest.mark.gui, pytest.mark.unit]


def test_param_tuning_toggle(loaded_fit, qapp):
    ctrl = loaded_fit._fitCtrl
    ctrl._paramTuningEnabled(False)
    qapp.processEvents()
    assert not loaded_fit._pageButtons["calibrate"].isEnabled()
    ctrl._paramTuningEnabled(True)
    qapp.processEvents()
    assert loaded_fit._pageButtons["calibrate"].isEnabled()
