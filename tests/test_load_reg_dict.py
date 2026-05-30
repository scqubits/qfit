"""Tests for qfit.utils.load_reg_dict."""
import pytest

from qfit.utils.load_reg_dict import _extract_version, parseRegDict


pytestmark = pytest.mark.unit


class TestExtractVersion:
    def test_extract_version_triple(self):
        assert _extract_version({"version": "3.0.1"}) == (3, 0, 1)

    def test_extract_version_missing_defaults(self):
        assert _extract_version({}) == (1, 0, 0)


class TestParseRegDict:
    def test_current_version_passthrough(self):
        reg = {"version": "3.0.0", "MeasDataSet.data": []}
        out = parseRegDict(reg)
        assert out["version"] == "3.0.0"

    def test_unsupported_major_zero(self):
        with pytest.raises(ValueError, match="no longer supported"):
            parseRegDict({"version": "0.9.0"})
