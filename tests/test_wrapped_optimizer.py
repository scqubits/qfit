"""Tests for qfit.utils.wrapped_optimizer."""
import pytest

from qfit.utils.wrapped_optimizer import Optimization


pytestmark = pytest.mark.unit


def _quadratic_cost(params):
    x = params["x"]
    y = params["y"]
    return (x - 1.0) ** 2 + (y - 2.0) ** 2


class TestOptimization:
    def test_lbfgsb_finds_minimum(self):
        opt = Optimization(
            fixed_variables={},
            free_variable_ranges={"x": [0.0, 2.0], "y": [0.0, 4.0]},
            target_func=_quadratic_cost,
            optimizer="L-BFGS-B",
            opt_options={"maxiter": 20},
        )
        result = opt.run(init_x={"x": 0.5, "y": 1.0})
        assert result.final_target == pytest.approx(0.0, abs=1e-2)
        final = result.final_para
        assert final["x"] == pytest.approx(1.0, abs=0.1)
        assert final["y"] == pytest.approx(2.0, abs=0.1)

    def test_fixed_parameter_respected(self):
        opt = Optimization(
            fixed_variables={"x": 1.0},
            free_variable_ranges={"y": [0.0, 4.0]},
            target_func=_quadratic_cost,
            optimizer="L-BFGS-B",
            opt_options={"maxiter": 15},
        )
        result = opt.run(init_x={"y": 0.5})
        assert result.final_full_para["x"] == pytest.approx(1.0, abs=1e-6)
