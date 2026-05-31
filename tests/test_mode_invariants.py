"""Tests for GUI mode invariants (pattern K)."""
import pytest

from tests.helpers import assert_mode_invariants, click_page_button, switch_page


pytestmark = [pytest.mark.gui, pytest.mark.unit]


class TestPageModeInvariants:
    @pytest.mark.parametrize("page", ["calibrate", "extract", "prefit", "fit"])
    def test_switch_page_maintains_invariants(self, loaded_fit, qapp, page):
        switch_page(loaded_fit, page)
        qapp.processEvents()
        assert_mode_invariants(loaded_fit)

    def test_leave_calibrate_interrupts_extraction(self, loaded_fit, qapp):
        loaded_fit._caliParamModel.caliStatus = True
        click_page_button(loaded_fit, "extract")
        qapp.processEvents()
        assert loaded_fit._caliParamModel.caliStatus is False

    def test_extract_page_sets_destination(self, loaded_fit, qapp):
        switch_page(loaded_fit, "extract")
        qapp.processEvents()
        assert loaded_fit._plottingCtrl.dataDestination == "EXTRACT"
