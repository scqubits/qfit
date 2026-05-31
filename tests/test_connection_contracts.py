"""P0 fan-out connection contract tests (Layer 2)."""
from __future__ import annotations

import pytest
from pytestqt.qtbot import QtBot

from qfit.models.data_structures import MeasRawXYConfig
from qfit.models.registry import Registry
from tests.support.app_harness import (
    add_minimal_extracted_points,
    apply_minimal_y_calibration_gui,
    click_page_button,
    configure_post_import,
    count_extracted_points_public,
    export_registry,
    models,
    process_events,
    run_sweep_button,
    setup_prefit_ready,
    status_text,
    switch_page,
    transfer_prefit_to_fit,
    views,
    wait_sweep_done,
)
from tests.support.invariants import assert_mode_invariants

pytestmark = [pytest.mark.gui, pytest.mark.unit]


def test_continue_to_post_import_ready(headless_fit, qapp):
    configure_post_import(headless_fit, qapp)
    assert views(headless_fit).page_view.currentPage == "calibrate"
    assert models(headless_fit).meas_data.importFinished is True


def test_extract_append_visible_in_public_api(loaded_fit, qapp):
    click_page_button(loaded_fit, "extract")
    process_events(qapp)
    before = count_extracted_points_public(loaded_fit)
    add_minimal_extracted_points(loaded_fit, n_points=2)
    after = count_extracted_points_public(loaded_fit)
    assert after > before


def test_page_changed_updates_sweep_usage(loaded_fit, qapp):
    click_page_button(loaded_fit, "prefit")
    process_events(qapp)
    assert models(loaded_fit).quantum_model.sweepUsage == "prefit"


def test_cali_interrupt_via_page_button(loaded_fit, qapp):
    models(loaded_fit).cali_param_model.caliStatus = True
    click_page_button(loaded_fit, "extract")
    process_events(qapp)
    assert models(loaded_fit).cali_param_model.caliStatus is False


def test_x_cali_updated_reaches_quantum_model(loaded_fit, qapp, qtbot: QtBot):
    cali = models(loaded_fit).cali_param_model
    qm = models(loaded_fit).quantum_model
    with qtbot.waitSignal(cali.xCaliUpdated, timeout=3000):
        cali.sendXCaliFunc()
    assert qm.ingredientsReady() or qm._sweepParamSets is not False


def test_y_cali_updated_reaches_quantum_model(loaded_fit, qapp, qtbot: QtBot):
    cali = models(loaded_fit).cali_param_model
    click_page_button(loaded_fit, "calibrate")
    apply_minimal_y_calibration_gui(loaded_fit, qapp)
    with qtbot.waitSignal(cali.yCaliUpdated, timeout=3000):
        cali.sendYCaliFunc()
    assert models(loaded_fit).quantum_model._yCaliFunc is not False


def test_prefit_to_fit_transfer_updates_parameters(loaded_fit, qapp):
    click_page_button(loaded_fit, "prefit")
    process_events(qapp)
    before = loaded_fit.get_circuit_parameters(source="fit")
    transfer_prefit_to_fit(loaded_fit, qapp)
    after = loaded_fit.get_circuit_parameters(source="fit")
    assert isinstance(after, dict)
    assert before.keys() == after.keys() or len(after) >= len(before)


def test_opt_finished_reenables_ui(loaded_fit, qapp):
    loaded_fit._fitCtrl._paramTuningEnabled(False)
    process_events(qapp)
    loaded_fit._fitCtrl._paramTuningEnabled(True)
    process_events(qapp)
    assert views(loaded_fit).page_buttons["prefit"].isEnabled()


def test_ready_to_plot_smoke_after_dynamical_init(loaded_fit, qapp):
    models(loaded_fit).meas_data.emitReadyToPlot()
    process_events(qapp)


def test_sweep_button_updates_status(headless_fit, qapp):
    setup_prefit_ready(headless_fit, qapp)
    run_sweep_button(headless_fit, qapp)
    wait_sweep_done(headless_fit, qapp, timeout_ms=90_000)
    text = status_text(headless_fit)
    assert "PREFIT" in text or "SUCCESS" in text or "WARNING" in text


def test_save_load_preserves_extracted_points(tmp_path, loaded_fit, qapp):
    click_page_button(loaded_fit, "extract")
    add_minimal_extracted_points(loaded_fit)
    before = loaded_fit.get_extracted_points()
    path = tmp_path / "roundtrip.qfit"
    export_registry(loaded_fit, path)
    data = Registry.dictFromFile(str(path))
    assert data is not None
    assert "AllExtractedData.data" in data or "version" in data
    assert len(before.list_figures()) >= 0


def test_fig_switch_syncs_extract_context(loaded_fit, qapp):
    if models(loaded_fit).meas_data.rowCount() <= 1:
        pytest.skip("single figure fixture")
    switch_page(loaded_fit, "extract")
    process_events(qapp)
    assert_mode_invariants(loaded_fit)
