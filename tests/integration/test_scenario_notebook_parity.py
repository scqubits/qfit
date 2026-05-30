"""Notebook / YAML script parity with GUI getters (slow)."""
import pytest

from tests.conftest import YAML_CONFIG
from tests.support.app_harness import configure_post_import

pytestmark = [pytest.mark.slow, pytest.mark.integration]


def test_yaml_config_lists_files():
    if not YAML_CONFIG.exists():
        pytest.skip("example_data/qfit_config.yaml not available")
    from qfit.utils.run_by_scripts import dataPathsFromYaml

    paths = dataPathsFromYaml(str(YAML_CONFIG))
    assert isinstance(paths, dict)


@pytest.mark.gui
def test_gui_post_import_exposes_hilbertspace(headless_fit, qapp):
    configure_post_import(headless_fit, qapp)
    assert headless_fit.get_hilbertspace(source="prefit") is not None
