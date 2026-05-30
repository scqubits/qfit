"""Tests for qfit.utils.run_by_scripts."""
from pathlib import Path

import pytest

from qfit.utils.run_by_scripts import combinePath, dataPathsFromYaml


pytestmark = pytest.mark.unit

YAML = Path(__file__).resolve().parents[1] / "example_data" / "qfit_config.yaml"


class TestCombinePath:
    def test_combine_relative(self):
        assert combinePath("/tmp/base", "data/file.h5") == "/tmp/base/data/file.h5"


@pytest.mark.skipif(not YAML.exists(), reason="qfit_config.yaml missing")
def test_data_paths_from_yaml():
    paths = dataPathsFromYaml(str(YAML))
    assert len(paths) >= 1
    assert all(str(p).endswith(".h5") for p in paths)


@pytest.mark.gui
def test_apply_import_on_headless_fit(headless_fit):
    from qfit.models.data_structures import MeasRawXYConfig
    from qfit.utils.run_by_scripts import applyImport

    meas = headless_fit._measData.currentMeasData
    applyImport(
        headless_fit,
        xAxis=[meas.rawXNames[0]],
        yAxis=[meas.rawYNames[0]],
        transposeSquareData=False,
    )
    assert headless_fit._pageView.currentPage == "calibrate"
