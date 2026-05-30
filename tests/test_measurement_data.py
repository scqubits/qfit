"""Tests for qfit.models.measurement_data readers."""
from pathlib import Path

import pytest

from qfit.models.measurement_data import GenericH5Reader, ImageFileReader, MatlabReader


pytestmark = pytest.mark.unit

REPO = Path(__file__).resolve().parents[1]
SYNTHETIC = REPO / "tests" / "fixtures" / "synthetic_twotone.h5"
EXAMPLE = REPO / "example_data"


@pytest.mark.skipif(not SYNTHETIC.exists(), reason="synthetic h5 missing")
def test_generic_h5_reader_synthetic():
    data = GenericH5Reader().fromFile(str(SYNTHETIC))
    assert data.name.endswith(".h5") or "synthetic" in data.name
    assert len(data.rawXNames) >= 1
    assert len(data.rawYNames) >= 1


@pytest.mark.skipif(
    not (EXAMPLE / "transmons.jpg").exists(), reason="example image missing"
)
def test_image_file_reader():
    data = ImageFileReader().fromFile(str(EXAMPLE / "transmons.jpg"))
    assert data.principalZ is not None


@pytest.mark.skipif(
    not (EXAMPLE / "spec_scan_flux_gate_20190629_v05.mat").exists(),
    reason="example mat missing",
)
def test_matlab_reader():
    data = MatlabReader().fromFile(
        str(EXAMPLE / "spec_scan_flux_gate_20190629_v05.mat")
    )
    assert len(data.rawXNames) >= 1
