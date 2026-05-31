"""Shared helpers for qfit GUI tests (re-exports from support layer)."""
from __future__ import annotations

import pytest

from tests.support.app_harness import (
    click_page_button,
    process_events,
    switch_page,
)
from tests.support.invariants import assert_all_invariants, assert_mode_invariants

__all__ = [
    "assert_mode_invariants",
    "assert_all_invariants",
    "switch_page",
    "click_page_button",
    "process_events",
    "assert_invariants",
]


@pytest.fixture
def assert_invariants():
    return assert_all_invariants
