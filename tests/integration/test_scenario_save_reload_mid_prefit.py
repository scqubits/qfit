"""Scenario: save and reload mid-prefit preserves public getters."""
import pytest

from qfit.models.registry import Registry
from tests.support.app_harness import (
    add_minimal_extracted_points,
    apply_minimal_y_calibration_gui,
    click_page_button,
    configure_post_import,
    open_qfit_file,
    shutdown_fit,
)

pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_save_reload_mid_prefit(tmp_path, headless_fit, qapp, fluxonium_resonator_hs, synthetic_h5_path):
    configure_post_import(headless_fit, qapp)
    click_page_button(headless_fit, "calibrate")
    apply_minimal_y_calibration_gui(headless_fit, qapp)
    click_page_button(headless_fit, "extract")
    add_minimal_extracted_points(headless_fit)
    click_page_button(headless_fit, "prefit")
    qapp.processEvents()

    before_points = headless_fit.get_extracted_points()
    before_params = headless_fit.get_circuit_parameters(source="prefit")
    path = tmp_path / "mid_prefit.qfit"
    headless_fit._registry.exportPkl(str(path))
    shutdown_fit(headless_fit, qapp)

    reloaded = open_qfit_file(path, deepcopy=True)
    qapp.processEvents()
    try:
        after_points = reloaded.get_extracted_points()
        after_params = reloaded.get_circuit_parameters(source="prefit")
        assert len(after_points.list_figures()) == len(before_points.list_figures())
        assert before_params.keys() == after_params.keys()
    finally:
        shutdown_fit(reloaded, qapp)

    data = Registry.dictFromFile(str(path))
    assert data is not None
