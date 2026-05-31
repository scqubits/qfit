"""Integration tests with synthetic fluxonium-resonator data."""
import pytest

from tests.support.app_harness import (
    add_minimal_extracted_points,
    click_page_button,
    configure_post_import,
    process_events,
    switch_page,
)
from tests.support.invariants import assert_mode_invariants

pytestmark = pytest.mark.integration


@pytest.mark.gui
def test_synthetic_workflow_smoke(headless_fit, qapp):
    configure_post_import(headless_fit, qapp)
    assert headless_fit._pageView.currentPage == "calibrate"
    switch_page(headless_fit, "extract")
    process_events(qapp)
    add_minimal_extracted_points(headless_fit)
    assert headless_fit._allDatasets.rowCount() >= 1
    switch_page(headless_fit, "prefit")
    process_events(qapp)
    assert_mode_invariants(headless_fit)
    hs = headless_fit.get_hilbertspace(deepcopy=True, source="prefit")
    assert hs is not None


@pytest.mark.gui
def test_public_export_apis_after_load(loaded_fit):
    cal = loaded_fit.get_calibration_result(source="prefit")
    assert cal is not None
    params = loaded_fit.get_circuit_parameters(source="prefit")
    assert isinstance(params, dict)
    points = loaded_fit.get_extracted_points()
    assert points is not None
