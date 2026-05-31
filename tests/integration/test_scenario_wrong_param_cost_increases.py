"""Scenario: wrong circuit parameter increases sweep cost."""
import pytest

from tests.support.app_harness import (
    get_cost,
    run_sweep_button,
    setup_prefit_ready,
    wait_sweep_done,
)

pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_wrong_ej_increases_cost(headless_fit, qapp):
    setup_prefit_ready(headless_fit, qapp)
    run_sweep_button(headless_fit, qapp)
    wait_sweep_done(headless_fit, qapp, timeout_ms=90_000)
    baseline = get_cost(headless_fit)
    assert baseline is not None

    # Nudge EJ away from truth
    hs_params = headless_fit._prefitHSParams
    ej_attr = None
    for parent, names in hs_params.paramNamesDict().items():
        if "EJ" in names:
            from qfit.models.data_structures import ParamAttr

            ej_attr = ParamAttr(parent, "EJ", "value", hs_params[parent]["EJ"].value * 0.85)
            break
    if ej_attr is not None:
        hs_params.storeParamAttr(ej_attr, fromSlider=True)
        hs_params.emitHSUpdated()
    qapp.processEvents()

    run_sweep_button(headless_fit, qapp)
    wait_sweep_done(headless_fit, qapp, timeout_ms=90_000)
    perturbed = get_cost(headless_fit)
    assert perturbed is not None
    assert perturbed >= baseline
