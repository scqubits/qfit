"""Async interaction chaos tests — sweep/fit interrupt paths."""
import pytest

from tests.support.app_harness import (
    click_page_button,
    models,
    process_events,
    run_sweep_button,
    setup_prefit_ready,
    switch_page,
    wait_sweep_done,
)
from tests.support.invariants import assert_all_invariants, assert_mode_invariants

pytestmark = [pytest.mark.chaos, pytest.mark.gui]


def test_fit_disables_page_buttons(loaded_fit, qapp):
    """During optimization lock, navigation buttons should be disabled."""
    loaded_fit._fitCtrl._paramTuningEnabled(False)
    qapp.processEvents()
    for page in ["calibrate", "extract", "prefit", "fit"]:
        assert not loaded_fit._pageButtons[page].isEnabled()
    loaded_fit._fitCtrl._paramTuningEnabled(True)
    qapp.processEvents()


def test_prefit_page_switch_survives(loaded_fit, qapp):
    switch_page(loaded_fit, "prefit")
    qapp.processEvents()
    switch_page(loaded_fit, "fit")
    qapp.processEvents()
    switch_page(loaded_fit, "prefit")
    qapp.processEvents()
    assert_mode_invariants(loaded_fit)


@pytest.mark.integration
def test_page_hop_during_sweep(headless_fit, qapp):
    fit = headless_fit
    setup_prefit_ready(fit, qapp)
    run_sweep_button(fit, qapp)
    click_page_button(fit, "extract")
    process_events(qapp)
    wait_sweep_done(fit, qapp, timeout_ms=90_000)
    assert_all_invariants(fit, qapp, skip=["K4", "K6"])
