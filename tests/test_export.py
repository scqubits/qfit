"""Tests for qfit.utils.export."""
import numpy as np
import pytest

from qfit.utils.export import (
    ExtractedPointsResult,
    FullCalibrationResult,
)


pytestmark = pytest.mark.unit


def _full_cali_result():
    return FullCalibrationResult(
        x_linear=np.array([[0.5]]),
        x_offset=np.array([0.25]),
        raw_dc_biases_names=("voltage",),
        mapped_sweep_params_names=("flux<br>(Fluxonium)",),
        y_slope=1e-3,
        y_offset=0.0,
        raw_y_name="freq",
    )


class TestFullCalibrationResult:
    def test_mapped_sweep_params_reference(self):
        cal = _full_cali_result()
        mapped = cal.get_mapped_sweep_params({"voltage": 0.0}, return_dict=True)
        assert mapped[("Fluxonium", "flux")] == pytest.approx(0.25)

    def test_mapped_y_affine(self):
        cal = _full_cali_result()
        assert cal.get_mapped_y(1000.0) == pytest.approx(1.0)

    def test_array_output(self):
        cal = _full_cali_result()
        arr = cal.get_mapped_sweep_params({"voltage": 0.0}, return_dict=False)
        assert arr.shape == (1,)


class TestExtractedPointsResult:
    def test_list_figures_and_transitions(self):
        data = {
            "fig1": {
                "0 - 2": {
                    "type": "NO_TAG",
                    "x": [0.1],
                    "y": [4.0],
                    "photons": None,
                    "initial_states": None,
                    "final_states": None,
                }
            }
        }
        result = ExtractedPointsResult(data)
        assert result.list_figures() == ["fig1"]
        assert result.list_transitions("fig1") == ["0 - 2"]

    def test_missing_figure_raises(self):
        result = ExtractedPointsResult({})
        with pytest.raises(KeyError):
            result.list_transitions("missing")
