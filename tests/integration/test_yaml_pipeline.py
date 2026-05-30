"""YAML pipeline import stage."""
from pathlib import Path

import pytest

from qfit.utils.run_by_scripts import dataPathsFromYaml


pytestmark = pytest.mark.integration

YAML = Path(__file__).resolve().parents[2] / "example_data" / "qfit_config.yaml"


@pytest.mark.skipif(not YAML.exists(), reason="qfit_config.yaml missing")
def test_yaml_lists_partial_twotone_files():
    paths = dataPathsFromYaml(str(YAML))
    assert len(paths) == 6
    assert all(Path(p).name.startswith("partial_twotone") for p in paths)
