"""Tests for qfit.models.data_structures."""
import numpy as np
import pytest

from qfit.models.data_structures import (
    MeasRawXYConfig,
    Status,
    Tag,
    ExtrTransition,
)


pytestmark = pytest.mark.unit


class TestTag:
    def test_no_tag_defaults(self):
        tag = Tag()
        assert tag.tagType == "NO_TAG"

    def test_dressed_transition_str(self):
        tag = Tag("DISPERSIVE_DRESSED", initial=[0], final=[2])
        assert "0" in tag.transitionStr()

    def test_tag_equality(self):
        a = Tag("NO_TAG")
        b = Tag("NO_TAG")
        assert a == b


class TestStatus:
    def test_status_str_contains_type(self):
        s = Status("test", "ready", message="ok")
        assert "ready" in str(s)


class TestMeasRawXYConfig:
    def test_config_stores_axes(self):
        cfg = MeasRawXYConfig(checkedX=["voltage"], checkedY=["freq"])
        assert cfg.checkedX == ["voltage"]
        assert cfg.checkedY == ["freq"]


class TestExtrTransition:
    def test_empty_transition(self):
        t = ExtrTransition(name="0 - 2")
        assert t.name == "0 - 2"
        assert t.count() == 0
