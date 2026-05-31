"""Integration tests for public Fit API."""
import pytest


pytestmark = [pytest.mark.integration, pytest.mark.gui]


def test_fit_import_smoke(qapp):
    import qfit
    from qfit import Fit

    assert hasattr(Fit, "new")
    assert qfit.__version__
