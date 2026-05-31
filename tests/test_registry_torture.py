"""Registry save/load torture tests (pattern R)."""
import pytest

from qfit.models.registry import Registry
from tests.helpers import assert_mode_invariants, switch_page


pytestmark = [pytest.mark.chaos, pytest.mark.gui]


def test_save_reload_after_navigation(tmp_path, loaded_fit, qapp):
    for page in ["extract", "prefit", "fit", "calibrate"]:
        switch_page(loaded_fit, page)
        qapp.processEvents()

    path = tmp_path / "chaos.qfit"
    loaded_fit._registry.exportPkl(str(path))
    data = Registry.dictFromFile(str(path))
    assert data is not None
    assert "MeasDataSet.data" in data
    assert "version" in data


def test_registry_survives_page_chaos(tmp_path, loaded_fit, qapp):
    switch_page(loaded_fit, "prefit")
    switch_page(loaded_fit, "extract")
    qapp.processEvents()
    assert_mode_invariants(loaded_fit)

    path = tmp_path / "after_chaos.qfit"
    loaded_fit._registry.exportPkl(str(path))
    reloaded = Registry.dictFromFile(str(path))
    assert reloaded is not None
