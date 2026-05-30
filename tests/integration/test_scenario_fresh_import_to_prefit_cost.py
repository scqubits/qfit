"""Scenario: fresh import through prefit sweep with cost oracle."""
import pytest

from tests.support.app_harness import (
    get_cost,
    run_sweep_button,
    setup_prefit_ready,
    wait_sweep_done,
)

pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_fresh_import_to_prefit_cost(headless_fit, qapp):
    setup_prefit_ready(headless_fit, qapp)
    run_sweep_button(headless_fit, qapp)
    wait_sweep_done(headless_fit, qapp, timeout_ms=90_000)
    cost = get_cost(headless_fit)
    assert cost is not None
    assert cost >= 0.0
