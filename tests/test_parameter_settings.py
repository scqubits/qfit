"""Tests for qfit.models.parameter_settings."""
import pytest

from qfit.models.parameter_settings import DEFAULT_PARAM_MINMAX, QSYS_PARAM_NAMES
from scqubits import Fluxonium, Oscillator


pytestmark = pytest.mark.unit


class TestParameterSettings:
    def test_default_minmax_bounds(self):
        assert DEFAULT_PARAM_MINMAX["EJ"]["min"] < DEFAULT_PARAM_MINMAX["EJ"]["max"]
        assert DEFAULT_PARAM_MINMAX["EC"]["min"] < DEFAULT_PARAM_MINMAX["EC"]["max"]

    def test_fluxonium_param_names(self):
        names = QSYS_PARAM_NAMES[Fluxonium]
        assert "EJ" in names
        assert names["EJ"] == ["EJ"]

    def test_oscillator_param_names(self):
        names = QSYS_PARAM_NAMES[Oscillator]
        assert "E_osc" in names
