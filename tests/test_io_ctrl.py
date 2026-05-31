"""Tests for qfit.controllers.io_ctrl save/load."""
import pytest

from qfit.models.registry import Registry


pytestmark = [pytest.mark.gui, pytest.mark.unit]


def test_registry_export_pkl_round_trip(tmp_path, loaded_fit):
    path = tmp_path / "session.qfit"
    loaded_fit._registry.exportPkl(str(path))
    loaded = Registry.dictFromFile(str(path))
    assert loaded is not None
    assert "version" in loaded


def test_io_save_via_registry_export(tmp_path, loaded_fit):
    path = tmp_path / "roundtrip.qfit"
    loaded_fit._registry.exportPkl(str(path))
    data = Registry.dictFromFile(str(path))
    assert data is not None
    assert "MeasDataSet.data" in data
