"""Tests for qfit.models.numerical_model.QuantumModel."""
import pytest


pytestmark = [pytest.mark.gui, pytest.mark.unit]


@pytest.fixture
def quantum_model(loaded_fit):
    return loaded_fit._quantumModel


class TestUpdateModeOnPageChange:
    @pytest.mark.parametrize(
        "page,expected",
        [
            ("prefit", "prefit"),
            ("fit", "fit"),
            ("calibrate", "none"),
            ("extract", "none"),
            ("setup", "none"),
        ],
    )
    def test_sweep_usage_follows_page(self, quantum_model, page, expected):
        quantum_model.updateModeOnPageChange(page)
        assert quantum_model.sweepUsage == expected


class TestReadyToOpt:
    def test_not_ready_without_extracted_data(self, quantum_model):
        assert quantum_model.readyToOpt is False
