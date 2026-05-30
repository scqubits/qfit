"""State-aware GUI fuzz engine for QFit."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, List, TYPE_CHECKING

from tests.support.app_harness import (
    add_minimal_extracted_points,
    apply_minimal_y_calibration_gui,
    click_page_button,
    models,
    process_events,
    run_sweep_button,
    switch_page,
    transfer_prefit_to_fit,
    views,
)
from tests.support.invariants import assert_all_invariants

if TYPE_CHECKING:
    from qfit.core.qfit import Fit
    from PySide6.QtWidgets import QApplication

# Fixed sequences from legacy test_chaos_navigation.py
LEGACY_FIXED_SEQUENCES = [
    ["calibrate", "extract", "calibrate"],
    ["extract", "prefit", "extract"],
    ["prefit", "fit", "prefit", "calibrate"],
    ["calibrate", "extract", "prefit", "fit", "calibrate"],
]


class FuzzState(Enum):
    POST_IMPORT = auto()
    CALI_IDLE = auto()
    EXTRACT = auto()
    PREFIT_IDLE = auto()
    SWEEP_RUNNING = auto()
    FIT_IDLE = auto()


@dataclass
class FuzzContext:
    state: FuzzState = FuzzState.POST_IMPORT
    has_extract: bool = False
    has_cali: bool = False


EventFn = Callable[["Fit", "QApplication", FuzzContext, random.Random], None]


def _page_hop(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    page = rng.choice(["calibrate", "extract", "prefit", "fit"])
    btn = views(fit).page_buttons.get(page)
    if btn is not None and btn.isEnabled():
        click_page_button(fit, page)
        process_events(qapp)
        if page == "calibrate":
            ctx.state = FuzzState.CALI_IDLE
        elif page == "extract":
            ctx.state = FuzzState.EXTRACT
        elif page == "prefit":
            ctx.state = FuzzState.PREFIT_IDLE
        elif page == "fit":
            ctx.state = FuzzState.FIT_IDLE


def _apply_y_cali(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    click_page_button(fit, "calibrate")
    process_events(qapp)
    apply_minimal_y_calibration_gui(fit, qapp)
    ctx.has_cali = True
    ctx.state = FuzzState.CALI_IDLE


def _append_extract(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    click_page_button(fit, "extract")
    process_events(qapp)
    add_minimal_extracted_points(fit, n_points=2)
    ctx.has_extract = True
    ctx.state = FuzzState.EXTRACT


def _new_extract_row(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    click_page_button(fit, "extract")
    process_events(qapp)
    views(fit).labeling_view.extractionCtrls["new"].click()
    process_events(qapp)


def _toggle_pan(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    models(fit).plotting_ctrl.togglePan()
    process_events(qapp)


def _toggle_select(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    models(fit).plotting_ctrl.toggleSelect()
    process_events(qapp)


def _toggle_calibrated_axes(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    cb = views(fit).calibrated_checkbox
    cb.setChecked(not cb.isChecked())
    process_events(qapp)


def _run_sweep(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    if not ctx.has_extract:
        _append_extract(fit, qapp, ctx, rng)
    click_page_button(fit, "prefit")
    process_events(qapp)
    if not ctx.has_cali:
        _apply_y_cali(fit, qapp, ctx, rng)
        click_page_button(fit, "prefit")
        process_events(qapp)
    run_sweep_button(fit, qapp)
    ctx.state = FuzzState.SWEEP_RUNNING


def _prefit_to_fit(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    click_page_button(fit, "prefit")
    process_events(qapp)
    transfer_prefit_to_fit(fit, qapp)
    click_page_button(fit, "fit")
    process_events(qapp)
    ctx.state = FuzzState.FIT_IDLE


def _cancel_cali_via_page(fit: Fit, qapp, ctx: FuzzContext, rng: random.Random) -> None:
    models(fit).cali_param_model.caliStatus = True
    click_page_button(fit, "extract")
    process_events(qapp)


LEGAL_EVENTS: dict[FuzzState, List[EventFn]] = {
    FuzzState.POST_IMPORT: [_page_hop, _apply_y_cali, _append_extract],
    FuzzState.CALI_IDLE: [_page_hop, _apply_y_cali, _cancel_cali_via_page, _toggle_calibrated_axes],
    FuzzState.EXTRACT: [_page_hop, _append_extract, _new_extract_row, _toggle_pan, _toggle_select],
    FuzzState.PREFIT_IDLE: [_page_hop, _run_sweep, _toggle_pan, _prefit_to_fit],
    FuzzState.SWEEP_RUNNING: [_page_hop, _toggle_pan],
    FuzzState.FIT_IDLE: [_page_hop, _prefit_to_fit],
}


def run_fuzz_sequence(
    fit: "Fit",
    qapp: "QApplication",
    rng: random.Random,
    n_steps: int,
    *,
    skip_k4: bool = False,
) -> None:
    ctx = FuzzContext(state=FuzzState.CALI_IDLE)
    skip = ["K4"] if skip_k4 else []
    skip = skip + ["K6", "K3"]  # fuzz may trigger async sweeps and expected cali/sim errors
    for _ in range(n_steps):
        events = LEGAL_EVENTS.get(ctx.state, [_page_hop])
        event = rng.choice(events)
        event(fit, qapp, ctx, rng)
        process_events(qapp)
        assert_all_invariants(fit, qapp, skip=skip)


def run_legacy_page_sequence(
    fit: "Fit",
    qapp: "QApplication",
    pages: List[str],
) -> None:
    for page in pages:
        btn = views(fit).page_buttons.get(page)
        if btn is not None and btn.isEnabled():
            switch_page(fit, page)
            process_events(qapp)
        assert_all_invariants(fit, qapp, skip=["K4", "K6"])
