"""Central harness for QFit GUI tests — sole owner of Fit private access."""
from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from qfit.models.data_structures import MeasRawXYConfig, Tag
from qfit.utils.helpers import OrderedDictMod

if TYPE_CHECKING:
    from qfit.core.qfit import Fit
    from scqubits.core.hilbert_space import HilbertSpace

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"
EXAMPLE_DATA = REPO_ROOT / "example_data"
SYNTHETIC_H5 = FIXTURES_DIR / "synthetic_twotone.h5"
QUICK_START_QFIT = EXAMPLE_DATA / "QFit_Quick_Start.qfit"
YAML_CONFIG = EXAMPLE_DATA / "qfit_config.yaml"

TRUTH_PARAMS = {
    "EJ": 3.2,
    "EC": 0.95,
    "EL": 0.23,
    "E_osc": 6.035,
    "g": 0.106,
}

GUESS_PARAMS = {
    "EJ": 3.0,
    "EC": 0.9,
    "EL": 0.25,
    "E_osc": 6.035,
    "g": 0.106,
}

COST_VALUE_RE = re.compile(
    r"(?:mean square error|root mean square error):\s+(\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s+(GHz(?:\u00B2)?|MHz(?:\u00B2)?)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class FitViews:
    page_view: Any
    calibration_view: Any
    labeling_view: Any
    sweep_settings_view: Any
    fit_view: Any
    fit_param_view: Any
    status_bar_view: Any
    page_buttons: Dict[str, Any]
    canvas_tools: Dict[str, Any]
    calibrated_checkbox: Any


@dataclass(frozen=True)
class FitModels:
    quantum_model: Any
    cali_param_model: Any
    all_datasets: Any
    active_dataset: Any
    meas_data: Any
    fit_model: Any
    fit_ctrl: Any
    plotting_ctrl: Any
    registry: Any


def build_headless_fit(
    hilbert_space: "HilbertSpace",
    measurement_file_name: str | None = None,
    deepcopy_hs: bool = False,
) -> "Fit":
    from qfit.core.qfit import Fit

    fit = Fit.__new__(Fit)
    fit._ioCtrl.newProject(
        fromMenu=False,
        hilbertSpace=hilbert_space,
        measurementFileName=measurement_file_name,
        deepcopy=deepcopy_hs,
    )
    disable_auto_run(fit)
    return fit


def open_qfit_file(path: str | Path, deepcopy: bool = True) -> "Fit":
    from qfit.core.qfit import Fit

    fit = Fit.__new__(Fit)
    fit._ioCtrl.openFile(fromMenu=False, fileName=str(path), deepcopy=deepcopy)
    disable_auto_run(fit)
    return fit


def disable_auto_run(fit: "Fit") -> None:
    if hasattr(fit, "_quantumModel"):
        fit._quantumModel._autoRun = False


def shutdown_fit(fit: "Fit", qapp: QApplication) -> None:
    """Best-effort cleanup; avoid MainWindow.close() which blocks under pytest."""
    if hasattr(fit, "_quantumModel"):
        fit._quantumModel._autoRun = False
        fit._quantumModel.sweepUsage = "none"
        fit._quantumModel._sweepThreadPool.clear()
    if hasattr(fit, "_fitModel"):
        fit._fitModel._fitThreadPool.clear()
    fit._mainWindow.hide()
    qapp.processEvents()


def views(fit: "Fit") -> FitViews:
    return FitViews(
        page_view=fit._pageView,
        calibration_view=fit._calibrationView,
        labeling_view=fit._labelingView,
        sweep_settings_view=fit._sweepSettingsView,
        fit_view=fit._fitView,
        fit_param_view=fit._fitParamView,
        status_bar_view=fit._statusBarView,
        page_buttons=fit._pageButtons,
        canvas_tools=fit._canvasTools,
        calibrated_checkbox=fit._mainUi.calibratedCheckBox,
    )


def models(fit: "Fit") -> FitModels:
    return FitModels(
        quantum_model=fit._quantumModel,
        cali_param_model=fit._caliParamModel,
        all_datasets=fit._allDatasets,
        active_dataset=fit._activeDataset,
        meas_data=fit._measData,
        fit_model=fit._fitModel,
        fit_ctrl=fit._fitCtrl,
        plotting_ctrl=fit._plottingCtrl,
        registry=fit._registry,
    )


def process_events(qapp: QApplication) -> None:
    qapp.processEvents()


def switch_page(fit: "Fit", page: str) -> None:
    fit._pageView.switchToPage(page)


def click_page_button(fit: "Fit", page: str) -> None:
    """Switch page via nav button (fires interruptCali hooks)."""
    fit._pageButtons[page].click()


def status_text(fit: "Fit") -> str:
    return fit._statusBarView.statusBarLabel.text()


def parse_cost_from_status(text: str) -> Optional[float]:
    """Extract numeric cost from status bar text (GHz or MHz units)."""
    match = COST_VALUE_RE.search(text)
    if not match:
        return None
    value = float(match.group(1))
    unit = match.group(2)
    if unit.startswith("MHz"):
        return value * 1e-3
    return value


def get_cost(fit: "Fit", *, forced: bool = True) -> Optional[float]:
    """Read cost from status bar, falling back to QuantumModel oracle."""
    cost = parse_cost_from_status(status_text(fit))
    if cost is not None:
        return cost
    qm = models(fit).quantum_model
    if qm.ingredientsReady():
        return float(qm.sweep2SpecCost(forced=forced))
    return None


def configure_post_import(fit: "Fit", qapp: QApplication) -> None:
    meas = fit._measData.currentMeasData
    fit._measData.storeRawXYConfig(
        MeasRawXYConfig(
            checkedX=[meas.rawXNames[0]],
            checkedY=[meas.rawYNames[0]],
        )
    )
    fit._measDataCtrl.continueToPostImportStages()
    disable_auto_run(fit)
    qapp.processEvents()


def add_minimal_extracted_points(fit: "Fit", n_points: int = 5) -> None:
    active = fit._activeDataset
    active.updateTag(Tag("DISPERSIVE_DRESSED", initial=[0], final=[2], photons=0))
    meas = fit._measData.currentMeasData
    x_name = meas.principalX.name
    y_name = meas.principalY.name
    xs = meas.principalX.data[::5]
    y_val = float(meas.principalY.data[len(meas.principalY.data) // 2])
    for x in xs[:n_points]:
        raw_x = meas.rawXByPrincipalX(float(x))
        active.append(
            OrderedDictMod({x_name: float(x), y_name: y_val}),
            raw_x,
        )


def apply_minimal_y_calibration_gui(fit: "Fit", qapp: QApplication) -> None:
    """Set linear Y calibration via calibration table line edits."""
    v = views(fit)
    meas = fit._measData.currentMeasData
    y_raw = meas.principalY.data
    raw_lo, raw_hi = float(y_raw[0]), float(y_raw[-1])
    v.calibration_view.rawYLineEdits["Y1"].setText(f"{raw_lo:.6f}")
    v.calibration_view.rawYLineEdits["Y2"].setText(f"{raw_hi:.6f}")
    v.calibration_view.mapYLineEdits["Y1"].setText(f"{raw_lo:.6f}")
    v.calibration_view.mapYLineEdits["Y2"].setText(f"{raw_hi:.6f}")
    for widget in (
        v.calibration_view.rawYLineEdits["Y1"],
        v.calibration_view.rawYLineEdits["Y2"],
        v.calibration_view.mapYLineEdits["Y1"],
        v.calibration_view.mapYLineEdits["Y2"],
    ):
        widget.editingFinished.emit()
    qapp.processEvents()
    models(fit).cali_param_model.sendYCaliFunc()
    qapp.processEvents()


def apply_minimal_x_calibration_model(fit: "Fit", qapp: QApplication) -> None:
    """Set partial 2-point X calibration via CaliParamModel (harness setup only)."""
    from qfit.models.data_structures import ParamAttr

    cali = fit._caliParamModel
    meas = fit._measData.currentMeasData
    fig = meas.name
    x_data = meas.principalX.data
    raw_lo, raw_hi = float(x_data[0]), float(x_data[-1])
    rows = cali._xRowIdxBySourceDict.get(fig, cali._caliTableXRowIdxList[:2])
    if len(rows) < 2:
        rows = cali._caliTableXRowIdxList[:2]
    raw_name = cali._rawXVecNameList[0]
    map_cols = [
        k
        for k in cali[rows[0]].keys()
        if k not in cali._rawXVecNameList and "DATA" not in k
    ]
    for row, raw_val, map_val in zip(rows[:2], [raw_lo, raw_hi], [0.0, 1.0]):
        cali.setParameter(row, raw_name, "value", raw_val)
        for col in map_cols:
            cali.storeParamAttr(ParamAttr(row, col, "value", str(map_val)))
    cali.sendXCaliFunc()
    qapp.processEvents()


def apply_minimal_x_calibration_gui(fit: "Fit", qapp: QApplication) -> None:
    """Set partial X calibration (2-point) for the current figure via GUI."""
    v = views(fit)
    meas = fit._measData.currentMeasData
    x_data = meas.principalX.data
    raw_lo, raw_hi = float(x_data[0]), float(x_data[-1])
    fig_name = meas.name
    line_set = v.calibration_view.lineEditSet.get(fig_name)
    if line_set is None:
        return
    raw_keys = [k for k in line_set if k != "mappedY" and "raw" in k.lower() or k.startswith("V")]
    if len(raw_keys) < 2:
        raw_keys = list(line_set.keys())[:2]
    if "mappedY" in line_set:
        pass
    # Use first sweep param row: raw endpoints map to 0.0 and 1.0 flux
    keys = [k for k in line_set if k not in ("mappedY",) and line_set[k] is not None]
    raw_edits = [line_set[k] for k in keys if hasattr(line_set[k], "setText")][:2]
    if len(raw_edits) >= 2:
        raw_edits[0].setText(f"{raw_lo:.6f}")
        raw_edits[1].setText(f"{raw_hi:.6f}")
        for w in raw_edits:
            w.editingFinished.emit()
    map_edits = v.calibration_view.mapXLineEdits
    map_keys = list(map_edits.keys())[:2] if map_edits else []
    if len(map_keys) >= 2:
        map_edits[map_keys[0]].setText("0.0")
        map_edits[map_keys[1]].setText("1.0")
        for k in map_keys[:2]:
            map_edits[k].editingFinished.emit()
    qapp.processEvents()
    models(fit).cali_param_model.sendXCaliFunc()
    qapp.processEvents()


def setup_prefit_ready(fit: "Fit", qapp: QApplication) -> None:
    """Import → cali → extract → prefit page with minimal data."""
    configure_post_import(fit, qapp)
    click_page_button(fit, "calibrate")
    qapp.processEvents()
    apply_minimal_y_calibration_gui(fit, qapp)
    apply_minimal_x_calibration_model(fit, qapp)
    click_page_button(fit, "extract")
    qapp.processEvents()
    add_minimal_extracted_points(fit)
    click_page_button(fit, "prefit")
    qapp.processEvents()


def wait_until(
    qapp: QApplication,
    predicate,
    timeout_ms: int = 30_000,
    interval_ms: int = 50,
) -> None:
    deadline = time.monotonic() + timeout_ms / 1000.0
    while time.monotonic() < deadline:
        qapp.processEvents()
        if predicate():
            return
        time.sleep(interval_ms / 1000.0)
    raise TimeoutError("wait_until timed out")


def wait_sweep_done(fit: "Fit", qapp: QApplication, timeout_ms: int = 60_000) -> None:
    qm = models(fit).quantum_model

    def done() -> bool:
        text = status_text(fit)
        if "ERROR:" in text:
            return True
        if "SUCCESS:" in text and "(PREFIT)" in text:
            return True
        if "WARNING:" in text and "(PREFIT)" in text:
            return True
        return not qm._sweepThreadPool.activeThreadCount()

    wait_until(qapp, done, timeout_ms=timeout_ms)


def wait_fit_done(fit: "Fit", qapp: QApplication, timeout_ms: int = 120_000) -> None:
    fm = models(fit).fit_model

    def done() -> bool:
        text = status_text(fit)
        if "ERROR:" in text and "(FIT)" in text:
            return True
        if "SUCCESS:" in text and "(FIT)" in text:
            return True
        return not fm._fitThreadPool.activeThreadCount()

    wait_until(qapp, done, timeout_ms=timeout_ms)


def run_sweep_button(fit: "Fit", qapp: QApplication) -> None:
    views(fit).sweep_settings_view.runSweep.click()
    qapp.processEvents()


def run_fit_button(fit: "Fit", qapp: QApplication) -> None:
    views(fit).fit_view.runFit.click()
    qapp.processEvents()


def transfer_prefit_to_fit(fit: "Fit", qapp: QApplication) -> None:
    views(fit).fit_view.dataTransferButtons["fit"].click()
    qapp.processEvents()


def export_registry(fit: "Fit", path: str | Path) -> None:
    fit._registry.exportPkl(str(path))


def extract_row_count(fit: "Fit") -> int:
    return fit._allDatasets.rowCount()


def extract_list_row_count(fit: "Fit") -> int:
    return fit._labelingView.extractionList.model().rowCount()


def count_extracted_points_public(fit: "Fit") -> int:
    points = fit.get_extracted_points()
    total = 0
    for fig in points.list_figures():
        for trans in points.list_transitions(fig):
            total += len(points[fig][trans]["x"])
    return total


def assert_public_api_consistent(fit: "Fit", tol: float = 1e-6) -> None:
    """Layer 4: extract list vs get_extracted_points()."""
    public_count = count_extracted_points_public(fit)
    list_rows = extract_list_row_count(fit)
    assert list_rows >= 1 or public_count == 0
    if public_count > 0:
        assert list_rows >= 1
