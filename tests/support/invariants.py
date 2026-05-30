"""Global GUI invariants (K0–K6) for fuzz and scenario tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Optional

from tests.support.app_harness import (
    assert_public_api_consistent,
    click_page_button,
    extract_list_row_count,
    models,
    status_text,
    views,
)

if TYPE_CHECKING:
    from qfit.core.qfit import Fit
    from PySide6.QtWidgets import QApplication

InvariantFn = Callable[["Fit", "QApplication"], None]


def assert_k1_page_mode(fit: "Fit") -> None:
    """Page ↔ controller mode consistency (pattern K)."""
    page = views(fit).page_view.currentPage
    pc = models(fit).plotting_ctrl
    qm = models(fit).quantum_model

    if page == "extract":
        assert pc.dataDestination == "EXTRACT"
    else:
        assert pc.dataDestination != "EXTRACT"

    if page == "prefit":
        assert qm.sweepUsage == "prefit"
    elif page == "fit":
        assert qm.sweepUsage == "fit"
    else:
        assert qm.sweepUsage == "none"


def assert_k2_cali_idle_off_page(fit: "Fit") -> None:
    page = views(fit).page_view.currentPage
    cali = models(fit).cali_param_model
    if page != "calibrate":
        assert cali.caliStatus is False


def assert_k3_thread_pools_bounded(fit: "Fit", qapp: "QApplication") -> None:
    qm = models(fit).quantum_model
    fm = models(fit).fit_model
    qapp.processEvents()
    assert qm._sweepThreadPool.activeThreadCount() <= 1
    assert fm._fitThreadPool.activeThreadCount() <= 1


def assert_k4_extract_consistency(fit: "Fit") -> None:
    assert_public_api_consistent(fit)


def assert_k5_nav_lock_consistent(fit: "Fit") -> None:
    """When fit is running, workflow nav buttons should be disabled."""
    fit_view = views(fit).fit_view
    page_buttons = views(fit).page_buttons
    if getattr(fit_view, "fitButtonMode", "run") == "stop":
        for page in ("calibrate", "extract", "prefit", "fit"):
            btn = page_buttons.get(page)
            if btn is not None:
                assert not btn.isEnabled()


def assert_k6_no_error_status(fit: "Fit", *, allow_error: bool = False) -> None:
    if allow_error:
        return
    text = status_text(fit)
    assert "ERROR:" not in text


def assert_all_invariants(
    fit: "Fit",
    qapp: "QApplication",
    *,
    allow_error_status: bool = False,
    skip: Optional[List[str]] = None,
) -> None:
    skip = skip or []
    checks: List[tuple[str, InvariantFn]] = [
        ("K1", lambda f, a: assert_k1_page_mode(f)),
        ("K2", lambda f, a: assert_k2_cali_idle_off_page(f)),
        ("K3", assert_k3_thread_pools_bounded),
        ("K4", lambda f, a: assert_k4_extract_consistency(f)),
        ("K5", lambda f, a: assert_k5_nav_lock_consistent(f)),
        ("K6", lambda f, a: assert_k6_no_error_status(f, allow_error=allow_error_status)),
    ]
    for name, fn in checks:
        if name in skip:
            continue
        fn(fit, qapp)


# Backward-compatible alias used by existing tests
def assert_mode_invariants(fit: "Fit") -> None:
    assert_k1_page_mode(fit)


def leave_calibrate_interrupts_cali(fit: "Fit", qapp: "QApplication") -> None:
    models(fit).cali_param_model.caliStatus = True
    click_page_button(fit, "extract")
    qapp.processEvents()
    assert models(fit).cali_param_model.caliStatus is False
