"""Tests for PlottingCtrl canvas routing (pattern P)."""
from unittest.mock import Mock

import pytest

from tests.support.app_harness import count_extracted_points_public, switch_page


pytestmark = [pytest.mark.gui, pytest.mark.unit]


def _mock_event(x, y):
    event = Mock()
    event.x = x
    event.y = y
    event.xdata = x
    event.ydata = y
    return event


class TestCanvasClickMonitoring:
    def test_none_destination_ignores_click(self, loaded_fit):
        pc = loaded_fit._plottingCtrl
        pc.dataDestination = "NONE"
        pc.clickResponse = "EXTRACT"
        before = count_extracted_points_public(loaded_fit)
        pc.canvasClickMonitoring(_mock_event(0.1, 4.0))
        assert count_extracted_points_public(loaded_fit) == before

    def test_pan_mode_ignores_extract(self, loaded_fit):
        pc = loaded_fit._plottingCtrl
        switch_page(loaded_fit, "extract")
        pc.setClickResponse("PAN")
        before = count_extracted_points_public(loaded_fit)
        pc.canvasClickMonitoring(_mock_event(0.1, 4.0))
        assert count_extracted_points_public(loaded_fit) == before

    def test_toggle_select_sets_extract_response(self, loaded_fit):
        pc = loaded_fit._plottingCtrl
        pc.toggleSelect()
        assert pc.clickResponse == "EXTRACT"
