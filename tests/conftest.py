"""Shared pytest fixtures for qfit."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import scqubits as scq
from PySide6.QtWidgets import QApplication, QMessageBox

import qfit.settings as qfit_settings
from tests.support.app_harness import (
    GUESS_PARAMS,
    QUICK_START_QFIT,
    TRUTH_PARAMS,
    YAML_CONFIG,
    build_headless_fit,
    configure_post_import,
    disable_auto_run,
    open_qfit_file,
    shutdown_fit,
)

# Re-export paths for tests that import from conftest
REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
EXAMPLE_DATA = REPO_ROOT / "example_data"
SYNTHETIC_H5 = FIXTURES_DIR / "synthetic_twotone.h5"

# Headless tests: never block on app.exec_()
qfit_settings.EXECUTED_IN_IPYTHON = True


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: fast pure or lightweight tests")
    config.addinivalue_line("markers", "gui: requires QApplication and widgets")
    config.addinivalue_line("markers", "integration: scqubits sweep or fit")
    config.addinivalue_line("markers", "slow: optional nightly job")
    config.addinivalue_line("markers", "chaos: navigation fuzz tests")
    config.addinivalue_line("markers", "chaos_long: extended fuzz (nightly)")


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv if sys.argv else ["pytest-qfit"])
    yield app


@pytest.fixture
def auto_dismiss_messagebox(monkeypatch):
    monkeypatch.setattr(QMessageBox, "exec", lambda self: QMessageBox.Yes)
    monkeypatch.setattr(QMessageBox, "exec_", lambda self: QMessageBox.Yes)


@pytest.fixture(scope="session")
def truth_params():
    return dict(TRUTH_PARAMS)


@pytest.fixture(scope="session")
def guess_params():
    return dict(GUESS_PARAMS)


@pytest.fixture(scope="session")
def fluxonium_resonator_hs(truth_params):
    fluxonium = scq.Fluxonium(
        EJ=truth_params["EJ"],
        EC=truth_params["EC"],
        EL=truth_params["EL"],
        flux=0.5,
        cutoff=40,
        truncated_dim=4,
        id_str="Fluxonium",
    )
    resonator = scq.Oscillator(
        E_osc=truth_params["E_osc"],
        l_osc=1.0,
        truncated_dim=3,
        id_str="Resonator",
    )
    hs = scq.HilbertSpace([fluxonium, resonator])
    hs.add_interaction(
        g=truth_params["g"],
        op1=fluxonium.n_operator,
        op2=resonator.annihilation_operator,
        add_hc=True,
        id_str="res-qubit",
    )
    return hs


@pytest.fixture(scope="session")
def synthetic_h5_path():
    if not SYNTHETIC_H5.exists():
        from tests.fixtures.generate_synthetic_h5 import write_synthetic_h5

        write_synthetic_h5(SYNTHETIC_H5)
    return str(SYNTHETIC_H5)


@pytest.fixture
def headless_fit(qapp, fluxonium_resonator_hs, synthetic_h5_path):
    """Fresh Fit on the import page."""
    fit = build_headless_fit(
        fluxonium_resonator_hs,
        measurement_file_name=synthetic_h5_path,
        deepcopy_hs=True,
    )
    disable_auto_run(fit)
    yield fit
    shutdown_fit(fit, qapp)


@pytest.fixture(scope="module")
def loaded_fit(qapp, fluxonium_resonator_hs, synthetic_h5_path):
    """Shared Fit past import — reused within a test module for speed."""
    fit = build_headless_fit(
        fluxonium_resonator_hs,
        measurement_file_name=synthetic_h5_path,
        deepcopy_hs=True,
    )
    configure_post_import(fit, qapp)
    yield fit
    shutdown_fit(fit, qapp)


@pytest.fixture(scope="module")
def opened_quick_start(qapp):
    if not QUICK_START_QFIT.exists():
        pytest.skip("example_data/QFit_Quick_Start.qfit not available")
    fit = open_qfit_file(QUICK_START_QFIT, deepcopy=True)
    qapp.processEvents()
    yield fit
    shutdown_fit(fit, qapp)


@pytest.fixture
def assert_invariants():
    from tests.support.invariants import assert_all_invariants

    return assert_all_invariants
