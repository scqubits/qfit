"""Tests for qfit.models.calibration.CaliParamModel."""
import pytest

from PySide6.QtCore import QCoreApplication


pytestmark = [pytest.mark.gui, pytest.mark.unit]


@pytest.fixture
def cali_model(qapp, loaded_fit):
    return loaded_fit._caliParamModel


class TestInterruptCali:
    def test_interrupt_clears_active_status(self, cali_model):
        cali_model.caliStatus = True
        cali_model.interruptCali()
        assert cali_model.caliStatus is False

    def test_interrupt_noop_when_inactive(self, cali_model):
        cali_model.caliStatus = False
        cali_model.interruptCali()
        assert cali_model.caliStatus is False


class TestCalibrationOnLoadedFit:
    def test_model_has_figure_names(self, cali_model, loaded_fit):
        names = [d.name for d in loaded_fit._measData.fullData]
        assert cali_model._figNames == names
