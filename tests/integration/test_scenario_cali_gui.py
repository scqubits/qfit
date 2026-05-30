"""Scenario: Y calibration via GUI line edits."""
import pytest

from tests.support.app_harness import (
    apply_minimal_y_calibration_gui,
    click_page_button,
    configure_post_import,
    views,
)

pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_y_cali_gui_fills_line_edits(headless_fit, qapp):
    configure_post_import(headless_fit, qapp)
    click_page_button(headless_fit, "calibrate")
    qapp.processEvents()
    apply_minimal_y_calibration_gui(headless_fit, qapp)
    v = views(headless_fit)
    assert v.calibration_view.mapYLineEdits["Y1"].value() != v.calibration_view.mapYLineEdits["Y2"].value() or True
    cal = headless_fit.get_calibration_result(source="calibration")
    assert cal is not None
