"""Scenario: prefit → fit parameter transfer."""
import pytest

from tests.support.app_harness import (
    click_page_button,
    process_events,
    transfer_prefit_to_fit,
)

pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_prefit_to_fit_transfer(loaded_fit, qapp):
    click_page_button(loaded_fit, "prefit")
    process_events(qapp)
    prefit_params = loaded_fit.get_circuit_parameters(source="prefit")
    transfer_prefit_to_fit(loaded_fit, qapp)
    fit_params = loaded_fit.get_circuit_parameters(source="fit")
    assert len(fit_params) >= len(prefit_params)
    for key, val in prefit_params.items():
        assert key in fit_params
