"""Optional notebook smoke (slow)."""
from pathlib import Path

import pytest


pytestmark = pytest.mark.slow

NOTEBOOK = (
    Path(__file__).resolve().parents[2]
    / "example_notebooks"
    / "QFit_Quick_Start.ipynb"
)


@pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook missing")
def test_notebook_is_valid_json():
    import json

    with open(NOTEBOOK) as f:
        nb = json.load(f)
    assert nb["nbformat"] >= 4
    assert len(nb["cells"]) > 5
