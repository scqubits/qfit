"""Tests for qfit.settings constants."""
import pytest

import qfit.settings as settings


pytestmark = pytest.mark.unit


def test_cost_function_type_valid():
    assert settings.COST_FUNCTION_TYPE in ("MSE", "RMSE")


def test_color_dict_has_expected_cmaps():
    assert "PuOr" in settings.color_dict
    assert "Cross" in settings.color_dict["PuOr"]
