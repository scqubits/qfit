"""Quick Start artifact regression (Layer 3)."""
import pytest

from tests.support.app_harness import (
    click_page_button,
    parse_cost_from_status,
    process_events,
    run_sweep_button,
    status_text,
    wait_sweep_done,
)
from tests.support.invariants import assert_all_invariants

pytestmark = [pytest.mark.integration, pytest.mark.gui]


@pytest.mark.parametrize("page", ["calibrate", "extract", "prefit", "fit"])
def test_quick_start_navigate_all_pages(opened_quick_start, qapp, page):
    click_page_button(opened_quick_start, page)
    process_events(qapp)
    assert_all_invariants(opened_quick_start, qapp, skip=["K4"])


def test_quick_start_export_apis(opened_quick_start):
    points = opened_quick_start.get_extracted_points()
    assert len(points.list_figures()) >= 1
    params = opened_quick_start.get_circuit_parameters(source="prefit")
    assert isinstance(params, dict)
    cal = opened_quick_start.get_calibration_result()
    assert cal is not None


@pytest.mark.slow
def test_quick_start_sweep_regression(opened_quick_start, qapp):
    click_page_button(opened_quick_start, "prefit")
    process_events(qapp)
    run_sweep_button(opened_quick_start, qapp)
    wait_sweep_done(opened_quick_start, qapp, timeout_ms=120_000)
    cost = parse_cost_from_status(status_text(opened_quick_start))
    assert cost is not None
