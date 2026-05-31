"""Full fresh-data E2E including fit (slow, nightly)."""
import pytest

from tests.support.app_harness import (
    parse_cost_from_status,
    process_events,
    run_sweep_button,
    setup_prefit_ready,
    status_text,
    transfer_prefit_to_fit,
    wait_fit_done,
    wait_sweep_done,
)
from tests.support.app_harness import click_page_button, run_fit_button

pytestmark = [pytest.mark.slow, pytest.mark.integration, pytest.mark.gui]


def test_full_e2e_synthetic(headless_fit, qapp, truth_params):
    setup_prefit_ready(headless_fit, qapp)
    run_sweep_button(headless_fit, qapp)
    wait_sweep_done(headless_fit, qapp, timeout_ms=90_000)
    cost = parse_cost_from_status(status_text(headless_fit))
    assert cost is not None

    transfer_prefit_to_fit(headless_fit, qapp)
    click_page_button(headless_fit, "fit")
    process_events(qapp)
    run_fit_button(headless_fit, qapp)
    wait_fit_done(headless_fit, qapp, timeout_ms=180_000)

    params = headless_fit.get_circuit_parameters(source="fit")
    ej_key = next((k for k in params if k[1] == "EJ"), None)
    if ej_key:
        assert abs(params[ej_key] - truth_params["EJ"]) < 0.5
